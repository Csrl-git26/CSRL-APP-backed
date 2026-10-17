import test from 'node:test';
import assert from 'node:assert/strict';
import { scopeChatData,makeCatalog,parseQuestion,validatePlan,analyzeChat,numberScore } from '../services/chatAnalysis.js';
const profile = (center,roll,name) => ({ centerCode:center,ROLL_KEY:roll,"STUDENT'S NAME":name,stream:'JEE' });
const marks = (center,roll,values) => ({ centerCode:center,ROLL_KEY:roll,stream:'JEE',...Object.fromEntries(values.map((v,i) => [`CMT0${i+1}_Physics`,v])) });
const data = {
 profiles:[profile('KNP','1','Asha'),profile('KNP','2','Bina'),profile('AGR','1','Chitra'),profile('KNP','3','Absent student')],
 tests:[marks('KNP','1',[60,45,30]),marks('KNP','2',[40,50,60]),marks('AGR','1',[30,40,50]),marks('KNP','3',[90,80,'Absent'])],testColumns:[]
};
const options = { role:'admin',stream:'JEE',branch:'MAIN' };
const cat=makeCatalog(data);
function run(q,c=cat,opts=options) {const p=parseQuestion(q,c);assert.ok(validatePlan(p,c));return analyzeChat(c,p,opts);}
test('named centre scope and centre+roll student identity are enforced',()=>{
 const c=scopeChatData(data,{role:'centre'},['KNP']);assert.equal(c.tests.length,3);assert.equal(c.profiles.length,3);
 const s=scopeChatData(data,{role:'student',centerCode:'AGR',id:'1'});assert.equal(s.tests.length,1);assert.equal(s.profiles[0]["STUDENT'S NAME"],'Chitra');
 assert.throws(()=>scopeChatData(data,{role:'centre',id:'centre'}),/named centre/);
 assert.throws(()=>scopeChatData(data,{role:'bog'}),/cannot use/);
});
test('attention reasons use real names and do not conflate duplicate rolls',()=>{
 const r=run('KNP centre students needing special attention in physics last 3 CMT tests');
 assert.equal(r.rows.length,1);assert.equal(r.rows[0][0],'Asha');assert.match(r.rows[0].at(-1),/Declined/);assert.match(r.answer,/1 student record/);
 assert.ok(!r.rows.flat().includes('Chitra'));assert.deepEqual(r.sources.map(s=>s.test),['CMT01','CMT02','CMT03']);
});
test('centre trends use a fixed cohort and expose changing participation',()=>{
 const r=run('Which centres improved in last 2 CMT tests in Physics?');
 assert.deepEqual(r.rows.map(r=>r[0]),['AGR']);assert.equal(r.rows[0][2],40);assert.equal(r.rows[0][3],50);
 assert.ok(r.notes.some(n=>n.includes('one change')));
 const all=run('Compare centre performance in Physics in last 3 CMT tests');
 const knp=all.rows.find(r=>r[0]==='KNP');assert.equal(knp[1],2);assert.deepEqual(knp.slice(2,5),[50,47.5,45]);assert.match(knp.at(-1),/CMT03: 2/);
});
test('zeros and negatives count, missing/absent/invalid do not',()=>{
 assert.equal(numberScore(0),0);assert.equal(numberScore('-5'),-5);
 for(const v of [null,undefined,'',' ','Absent','AB','4x',false]) assert.equal(numberScore(v),null);
});
test('explicit below-mark threshold and decline follow-up',()=>{
 const p=parseQuestion('KNP students needing attention Physics below 50 marks last 3 CMT tests',cat);
 assert.equal(p.threshold,50);assert.equal(analyzeChat(cat,p,options).rows.length,1);
 const follow=parseQuestion('Show only declining students',cat,p);assert.equal(follow.intent,'attention');assert.equal(follow.threshold,50);assert.deepEqual(follow.centers,['KNP']);assert.equal(analyzeChat(cat,follow,options).rows[0][0],'Asha');
 // Follow-up must preserve an existing student attention intent.
});
test('student login cannot receive centre comparison or other names',()=>{
 const s=makeCatalog(scopeChatData(data,{role:'student',centerCode:'KNP',id:'1'}));
 const out=run('Which centres improved in last 2 CMT tests Physics',s,{...options,role:'student'});
 assert.equal(out.rows.length,0);assert.match(out.answer,/own marks/);
 const own=run('Show my student progress Physics last 3 CMT tests',s,{...options,role:'student'});assert.equal(own.rows[0][0],'Asha');
});
test('untrusted plans cannot request other centres, tests or database expressions',()=>{
 const permitted=makeCatalog(scopeChatData(data,{role:'centre'},['KNP']));
 const valid=parseQuestion('KNP attention Physics last 3 CMT tests',permitted);
 assert.equal(validatePlan({...valid,centers:['AGR']},permitted),null);
 assert.equal(validatePlan({...valid,testIds:['SECRET01']},permitted),null);
 assert.equal(validatePlan({...valid,count:999},permitted),null);
 assert.equal(validatePlan({...valid,threshold:{$gt:0}},permitted),null);
 assert.equal(validatePlan({...valid,subject:'$where'},permitted),null);
});
test('no cross-stream marks and no comparisons between different series',()=>{
 const mixed={...data,tests:[...data.tests,{centerCode:'MED',ROLL_KEY:'M1',stream:'NEET',NCT01_Physics:150,CMT01_Physics:90}]};
 const jee=makeCatalog(mixed,'JEE');assert.equal(jee.centers.includes('MED'),false);
 const neet=makeCatalog(mixed,'NEET');assert.deepEqual(neet.tests,['NCT01']);
 const multi=makeCatalog({...data,tests:[...data.tests, {...marks('KNP','4',[40,50,60]),FMT01_Physics:70}]});
 assert.match(run('KNP attention Physics',multi).answer,/Which test series/);
});
test('all missing latest marks do not create a false attention flag',()=>{
 const c=makeCatalog({profiles:[profile('KNP','1','A')],tests:[marks('KNP','1',[60,40,null])]});
 const r=run('KNP attention Physics last 3 CMT tests',c);assert.equal(r.rows.length,0);assert.match(r.answer,/no usable mark/);
});

test('new centre comparison does not inherit previous single-centre filters',()=>{ const p=parseQuestion('KNP attention Physics last 3 CMT tests',cat); const next=parseQuestion('Which centres improved in last 2 CMT tests?',cat,p);assert.deepEqual(next.centers,[]); });
