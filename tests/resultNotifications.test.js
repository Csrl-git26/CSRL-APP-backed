import test from 'node:test';
import assert from 'node:assert/strict';
import express from 'express';
import ExcelJS from 'exceljs';
import { validateSelection, recipientList, createResultNotificationsRouter, createNotificationWorker } from '../routes/resultNotifications.js';
import { renderEmail, reportWorkbook, SENDER } from '../services/resultNotificationEmail.js';
import { buildQualificationSummary, qualificationMetrics } from '../services/resultNotificationAnalysis.js';
const selection = { testKey: 'CMT01', stream: 'JEE', branch: 'MAIN', testDate: '2026-10-29', audience: 'all' };
const report = { stream: 'JEE', subjects: ['Physics','Chemistry','Math'], rows: [{ rank: 1, code: '<script>alert(1)</script>', appeared: 3, qualified: 1, Total: 123.456, Physics: 0 }], overall: { code: 'OVERALL', appeared: 3, qualified: 1, Total: 123.456 }, warnings: [] };
test('validates scope and dates; deduplicates recipients across login groups',async () => {
  assert.deepEqual(validateSelection(selection),selection);
  for (const input of [{ testDate: '2026-02-30' },{ audience: 'student' },{ testKey: 'A,B' },{ branch: 'OTHER' }]) assert.throws(() => validateSelection({ ...selection,...input }));
  const result = await recipientList('all',{ list: async role => [{ userId: 'USER@csrl.in', name: role },{ userId: 'not-an-email' }] });
  assert.equal(result.recipients.length,1); assert.equal(result.recipients[0].email,'user@csrl.in'); assert.deepEqual(result.recipients[0].roles,['centre','admin']); assert.deepEqual(result.skippedUsers,['not-an-email']);
});
test('email escapes data; Excel has merged red headers and numeric one-decimal metrics',async () => {
  const mail = renderEmail(selection,report);
  assert.match(mail.subject,/प्रगति/); assert.ok(!mail.html.includes('<script>')); assert.match(mail.html,/&lt;script&gt;/); assert.match(mail.html,/123\.5/); assert.match(mail.html,/automatically generated/);
  const book = new ExcelJS.Workbook(); await book.xlsx.load(await reportWorkbook(report));
  const sheet=book.worksheets[0];
  assert.equal(sheet.getCell('E3').value,null); // missing attempt remains blank
  assert.equal(sheet.getCell('G3').value,0); assert.equal(sheet.getCell('G3').numFmt,'0.0');
  assert.equal(sheet.getCell('A1').fill.fgColor.argb,'FFB91C1C'); assert.equal(sheet.getCell('A2').master.address,'A1');
  assert.match(renderEmail({ ...selection,stream:'NEET' },{ ...report,stream:'NEET',subjects:['Physics','Chemistry','Botany','Zoology'] }).html,/Expected MBBS admission/);
});
test('overall average is student weighted; raw accuracy pools attempts and retains zeros',() => {
  const profiles=[{ROLL_KEY:'1',centerCode:'A'},{ROLL_KEY:'2',centerCode:'A'},{ROLL_KEY:'3',centerCode:'B'}];
  const tests=[{ROLL_KEY:'1',CMT01:30},{ROLL_KEY:'2',CMT01:60},{ROLL_KEY:'3',CMT01:90}];
  const summary=buildQualificationSummary({profiles,tests},[{code:'A',tested:2,avg:45},{code:'B',tested:1,avg:90}],'CMT01','JEE');
  assert.equal(summary.overall.Total,60);
  const raw=[{studentId:'1',testId:'CMT01',marks:{1:4,2:-1,3:0}},{studentId:'2',testId:'CMT01',marks:{1:4,2:0,3:0}}];
  const result=qualificationMetrics({profiles},'CMT01','JEE',raw,[{testId:'CMT01',topics:[{subject:'PHYSICS',questions:[1,2,3]}]}]);
  assert.equal(result.overall.Physics_Attempted,1.5); assert.ok(Math.abs(result.overall.Physics_Accuracy-200/3)<1e-10);
});
test('HTTP routes require admin, setup, confirmation, and reconciled report before queueing',async t => {
  const oldKey=process.env.RESEND_API_KEY, oldEnabled=process.env.RESULT_EMAIL_ENABLED;
  t.after(() => { if(oldKey===undefined) delete process.env.RESEND_API_KEY; else process.env.RESEND_API_KEY=oldKey; if(oldEnabled===undefined) delete process.env.RESULT_EMAIL_ENABLED; else process.env.RESULT_EMAIL_ENABLED=oldEnabled; });
  let queued=0;
  const c={_id:'a'.repeat(64),report:{warnings:['Mismatch']},recipients:[{email:'user@csrl.in',status:'pending'}],state:'draft'};
  const Model={findById:()=>({lean:async()=>c}),updateOne:async()=>{queued++;}};
  const app=express(); app.use(express.json()); app.use((req,res,next)=>{req.user={role:req.headers['x-role']||'admin'};next();});
  app.use(createResultNotificationsRouter(async()=>report,{Model}));
  const server=app.listen(0,'127.0.0.1'); await new Promise(r=>server.once('listening',r)); t.after(()=>server.close());
  const url=`http://127.0.0.1:${server.address().port}/${c._id}/send`;
  const post=(body,role='admin')=>fetch(url,{method:'POST',headers:{'Content-Type':'application/json','x-role':role},body:JSON.stringify(body)});
  assert.equal((await post({confirm:'SEND'},'centre')).status,403);
  delete process.env.RESEND_API_KEY; process.env.RESULT_EMAIL_ENABLED='false'; assert.equal((await post({confirm:'SEND'})).status,503);
  process.env.RESEND_API_KEY='test-placeholder'; process.env.RESULT_EMAIL_ENABLED='true';
  assert.equal((await post({})).status,400); assert.equal((await post({confirm:'SEND'})).status,400); assert.equal(queued,0);
  c.report.warnings=[]; assert.equal((await post({confirm:'SEND'})).status,200); assert.equal(queued,1);
});
test('worker sends privately, preserves retry key, never resends accepted recipients, expires unsafe retries',async () => {
  const recipient={email:'user@csrl.in',status:'pending'};
  const c={_id:'b'.repeat(64),selection,recipients:[recipient],state:'queued',subject:'Test',html:'<p>Test</p>',text:'Test',filename:'test.xlsx',attachment:'test'};
  const Model={
    findOne:()=>({sort:()=>({lean:async()=>c.state==='queued'?c:null})}),
    updateOne:async (filter,update)=>{
      const criteria=filter.recipients?.$elemMatch;
      if(criteria?.$or && !['pending','sending'].includes(recipient.status)) return {modifiedCount:0};
      if(criteria?.lockUntil && recipient.lockUntil !== criteria.lockUntil) return {modifiedCount:0};
      if(filter.recipients?.$not && ['pending','sending'].includes(recipient.status)) return {modifiedCount:0};
      for(const [key,value] of Object.entries(update.$set)) {if(key.startsWith('recipients.$.')) recipient[key.slice(13)]=value; else c[key]=value;}
      return {modifiedCount:1};
    },
  };
  const calls=[];
  const tick=createNotificationWorker({Model,service:{list:async()=>[{userId:recipient.email}]},enabled:()=>true,send:async(url,options)=>{calls.push(options);if(calls.length===1)throw new Error('network');return{ok:true,status:200,json:async()=>({id:'provider-123'})};}});
  await tick(); assert.equal(recipient.status,'failed');
  recipient.status='pending'; await tick(); assert.equal(recipient.status,'sent');
  assert.equal(calls[0].headers['Idempotency-Key'],calls[1].headers['Idempotency-Key']);
  const message=JSON.parse(calls[1].body);assert.deepEqual(message.to,['user@csrl.in']);assert.ok(message.from.includes(SENDER));assert.equal(message.attachments[0].filename,'test.xlsx');
  await tick(); await tick(); assert.equal(calls.length,2);
  c.state='queued'; recipient.status='pending'; recipient.firstAttempt=new Date(Date.now()-24*60*60*1000);
  await tick(); assert.equal(recipient.status,'review'); assert.equal(calls.length,2);
});
