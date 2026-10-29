import test from 'node:test';
import assert from 'node:assert/strict';
import express from 'express';
import {parseAdvancedAttemptRows,aggregateAttemptRecords,advancedMetricsFromSheets,applyAdvancedChartMetrics} from '../services/advancedAttemptService.js';
import {createAdvancedAttemptsRouter} from '../routes/advancedAttempts.js';
const headers=['name','Roll Number','stream','centre','total_questions','not_attempted','attempted','incorrect','correct','ACC%'];
const row=['Student A',2701079,'JEE','KNP',96,6,90,31,59,65.56];
const profiles=[{ROLL_KEY:'2701079',centerCode:'KNP',stream:'JEE'},{ROLL_KEY:'2',centerCode:'DEL',stream:'JEE'}];
const rows=[headers,row];
test('validates counts format, unknown profiles, centres, duplicates, count totals and rounded ACC%',()=>{
 const records=parseAdvancedAttemptRows([...rows,Array(10).fill(null)],profiles);assert.equal(records.length,1);assert.equal(records[0].roll,'2701079');assert.equal(aggregateAttemptRecords(records).Total_Accuracy,59/90*100);
 for(const [index,value] of [[1,'999'],[3,'DEL'],[2,'NEET'],[5,7],[7,30],[8,59.5],[6,-1],[9,99]]){const bad=[...row];bad[index]=value;assert.throws(()=>parseAdvancedAttemptRows([headers,bad],profiles));}
 assert.throws(()=>parseAdvancedAttemptRows([...rows,row],profiles),/duplicate/);assert.throws(()=>parseAdvancedAttemptRows(rows,[]),/must match/);
 assert.throws(()=>parseAdvancedAttemptRows([headers.filter(h=>h!=='correct'),row],profiles),/Missing columns/);
});
test('zero attempts are valid and aggregate accuracy is pooled, not a mean of percentages',()=>{
 const zero=[...row];zero[5]=96;zero[6]=zero[7]=zero[8]=zero[9]=0;assert.equal(aggregateAttemptRecords(parseAdvancedAttemptRows([headers,zero],profiles)).Total_Accuracy,0);
 const records=[{roll:'2701079',centre:'KNP',attempted:2,correct:1},{roll:'2',centre:'DEL',attempted:8,correct:8},{roll:'unknown',centre:'KNP',attempted:100,correct:100}];
 const metrics=advancedMetricsFromSheets([{records}],profiles);assert.equal(metrics.overall.Total_Accuracy,90);assert.equal(metrics.overall.Total_Attempted,5);assert.equal(metrics.overall.records,2);assert.equal(metrics.centres.KNP.Total_Accuracy,50);assert.equal(metrics.overall.Physics_Accuracy,null);
});
test('Advanced override preserves marks/rank; missing data or DB failure cannot expose marks-based attempts',async()=>{
 const data=[{name:'ADV01',Total:75,Total_Rank:4,Total_Attempted:25,Total_Accuracy:100,Physics_Attempted:10}];
 const Model={find:()=>({lean:async()=>[{_id:'ADV01',records:parseAdvancedAttemptRows(rows,profiles)}]})};
 await applyAdvancedChartMetrics(data,{stream:'JEE',branch:'ADVANCED',profiles,roll:'2701079',centre:'KNP'},Model);
 assert.equal(data[0].Total,75);assert.equal(data[0].Total_Rank,4);assert.equal(data[0].Total_Attempted,90);assert.equal(data[0].Total_Accuracy,59/90*100);assert.equal(data[0].Physics_Attempted,null);
 await applyAdvancedChartMetrics(data,{stream:'JEE',branch:'ADVANCED',profiles,roll:'2',centre:'DEL'},Model);assert.equal(data[0].Total_Attempted,null);
 await assert.rejects(applyAdvancedChartMetrics(data,{stream:'JEE',branch:'ADVANCED',profiles,centre:'KNP'},{find:()=>({lean:async()=>{throw Error('offline');}})}));assert.equal(data[0].Total_Accuracy,null);
});
test('Main and NEET remain byte-for-byte unchanged without querying Advanced storage',async()=>{
 for(const [stream,branch] of [['JEE','MAIN'],['NEET','MAIN'],['NEET','ADVANCED']]){
  const data=[{name:'MT01',Total_Attempted:20,Physics_Accuracy:50}];const original=structuredClone(data);
  await applyAdvancedChartMetrics(data,{stream,branch},{find:()=>{throw Error('must not query');}});assert.deepEqual(data,original);
 }
});
test('HTTP requires admin and Advanced catalog, validates all rows and replaces atomically with a version check',async t=>{
 let saved=null,writes=0;
 const Model={findById:()=>({lean:async()=>saved}),create:async data=>{if(saved)throw Object.assign(Error('duplicate'),{code:11000});writes++;saved=data;},findOneAndUpdate:(query,update)=>({lean:async()=>{if(saved?.version!==query.version)return null;writes++;saved={...saved,...update.$set};return saved;}})};
 const Catalog={findOne:({testId})=>({lean:async()=>testId==='ADV01'?{stream:'JEE',branch:'ADVANCED'}:{stream:'JEE',branch:'MAIN'}})};
 const app=express();app.use(express.json());app.use((req,res,next)=>{req.user={role:req.headers['x-role']||'admin',id:'admin'};next();});app.use(createAdvancedAttemptsRouter({Model,Catalog,loadData:async()=>({profiles})}));
 const server=app.listen(0,'127.0.0.1');await new Promise(r=>server.once('listening',r));t.after(()=>server.close());const root=`http://127.0.0.1:${server.address().port}`;
 const post=(path,body,role='admin')=>fetch(root+path,{method:'POST',headers:{'Content-Type':'application/json','x-role':role},body:JSON.stringify({stream:'JEE',branch:'ADVANCED',testId:'ADV01',rows,...body})});
 assert.equal((await post('/preview',{},'centre')).status,403);
 for(const body of [{branch:'MAIN'},{stream:'NEET'},{testId:'MT01'}])assert.equal((await post('/preview',body)).status,400);
 assert.equal((await post('/preview',{})).status,200);assert.equal(writes,0);assert.equal((await post('/',{})).status,400);
 assert.equal((await post('/',{confirm:'UPLOAD',rows:[headers,[...row.slice(0,9),99]]})).status,400);assert.equal(writes,0);
 assert.equal((await post('/',{confirm:'UPLOAD'})).status,200);assert.equal(writes,1);assert.equal((await post('/',{confirm:'UPLOAD'})).status,409);assert.equal((await post('/',{confirm:'UPLOAD',version:'stale'})).status,409);assert.equal(writes,1);
 const version=saved.version;assert.equal((await post('/',{confirm:'UPLOAD',version})).status,200);assert.equal(writes,2);assert.notEqual(saved.version,version);assert.equal(saved.records.length,1);
});
test('subject columns including repeated ACC% validate and produce independent subject metrics',async()=>{
 const subjectHeaders=['physics','chemistry','mathematics'].flatMap(s=>[s+'_total',s+'_attempted',s+'_not_attempted',s+'_correct','ACC%',s+'_incorrect']);
 const detailed=[...row,32,31,1,22,70.97,9,32,30,2,22,73.33333333,8,32,29,3,15,51.72,14];
 const fullHeaders=[...headers,...subjectHeaders];
 const records=parseAdvancedAttemptRows([fullHeaders,detailed],profiles);
 const metrics=aggregateAttemptRecords(records);
 assert.equal(metrics.Physics_Attempted,31);assert.equal(metrics.Chemistry_Accuracy,22/30*100);assert.equal(metrics.Math_Accuracy,15/29*100);
 const bad=[...detailed];bad[14]=65.56;assert.throws(()=>parseAdvancedAttemptRows([fullHeaders,bad],profiles),/Physics ACC/);
 const mismatch=[...detailed];mismatch[11]=30;mismatch[12]=2;mismatch[15]=8;mismatch[14]=22/30*100;
 assert.throws(()=>parseAdvancedAttemptRows([fullHeaders,mismatch],profiles),/add up/);
 assert.throws(()=>parseAdvancedAttemptRows([fullHeaders.slice(0,-1),detailed],profiles),/Missing or duplicate/);
 const chart=[{name:'ADV01',Physics:90}];await applyAdvancedChartMetrics(chart,{stream:'JEE',branch:'ADVANCED',profiles,roll:'2701079'},{find:()=>({lean:async()=>[{_id:'ADV01',records}]})});assert.equal(chart[0].Physics_Attempted,31);assert.equal(chart[0].Physics_Correct,22);assert.equal(chart[0].Physics,90);
 const legacy=parseAdvancedAttemptRows(rows,profiles);assert.equal(aggregateAttemptRecords([...records,...legacy]).Physics_Attempted,null);
 const {default:Model}=await import('../models/AdvancedAttemptSheet.js');const doc=new Model({_id:'ADV01',version:'v',records});assert.equal(doc.records[0].subjects.Physics.correct,22);assert.equal(doc.validateSync(),undefined);
});
