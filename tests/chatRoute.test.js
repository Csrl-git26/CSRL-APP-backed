import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import vm from 'node:vm';
import * as analysis from '../services/chatAnalysis.js';

async function route({ user, body, ai = null, assigned = ['KNP'] }) {
  let handler, loads = 0;
  const data = {profiles:[{centerCode:'KNP',ROLL_KEY:'1',stream:'JEE',"STUDENT'S NAME":'Permitted Student'},{centerCode:'AGR',ROLL_KEY:'1',stream:'JEE',"STUDENT'S NAME":'Other Student'}],tests:[{centerCode:'KNP',ROLL_KEY:'1',stream:'JEE',CMT01_Physics:50,CMT02_Physics:30},{centerCode:'AGR',ROLL_KEY:'1',stream:'JEE',CMT01_Physics:20,CMT02_Physics:40}],testColumns:[]};
  const modules = {
    express: {default:{Router:()=>({get(){},post(_path,h){handler=h;}})}},
    '../services/dbService.js':{loadApplicationData:async()=>{loads++;return data;}},
    '../services/portalUserService.js':{portalUsers:{list:async()=>[{userId:'named',centres:assigned}]}},
    '../services/testBranchService.js':{TestBranch:{find:()=>({lean:async()=>[]})},scopeApplicationData:d=>d},
    '../services/chatAnalysis.js':analysis,
    '../services/chatAI.js':{aiConfigured:()=>!!ai,askAI:async()=>ai,PLANNER_PROMPT:'test',readPlan:s=>{try{return JSON.parse(s);}catch{return null;}}}
  };
  const ctx=vm.createContext({console,Date,Map,Set});
  const mod=new vm.SourceTextModule(await fs.readFile(new URL('../routes/chat.js',import.meta.url),'utf8'),{context:ctx});
  await mod.link(id=>{const exports=modules[id];return new vm.SyntheticModule(Object.keys(exports),function(){for(const [k,v] of Object.entries(exports))this.setExport(k,v);},{context:ctx});});
  await mod.evaluate();
  let result, status=200;
  const res={set(){return this;},status(n){status=n;return this;},json(v){result=v;return this;}};
  await handler({user,body},res);
  return {result,status,loads};
}
test('route denies unassigned shared centre before fetching any data',async()=>{
 const r=await route({user:{role:'centre',id:'centre'},body:{question:'KNP Physics attention'}});assert.equal(r.status,403);assert.equal(r.loads,0);
});
test('route falls back when AI returns invalid JSON and retains permitted data only',async()=>{
 const r=await route({user:{role:'centre',id:'centre',loginUserId:'named'},body:{question:'KNP centre student progress roll 1 Physics last 2 CMT tests'},ai:'not json'});
 assert.equal(r.status,200);assert.equal(r.result.mode,'database');assert.equal(r.result.rows[0][0],'Permitted Student');assert.ok(!JSON.stringify(r.result).includes('Other Student'));
});
test('AI cannot broaden scope through invented centre plan',async()=>{
 const p=analysis.parseQuestion('AGR student progress roll 1 Physics last 2 CMT tests',analysis.makeCatalog({profiles:[],tests:[{centerCode:'AGR',ROLL_KEY:'1',CMT01_Physics:20,CMT02_Physics:40}]}));
 const r=await route({user:{role:'centre',id:'centre',loginUserId:'named'},body:{question:'AGR centre student progress roll 1 Physics last 2 CMT tests'},ai:JSON.stringify(p)});
 assert.equal(r.status,200);assert.equal(r.result.rows.length,0);assert.match(r.result.answer,/unavailable/);
});
test('unsupported percentage thresholds cannot silently become raw-mark criteria',async()=>{
 const r=await route({user:{role:'admin',id:'admin'},body:{question:'KNP Physics students below 40% last 2 CMT tests'}});
 assert.equal(r.result.rows.length,0);assert.match(r.result.answer,/not yet supported/);
});
test('invalid stream and oversized question fail before reading records',async()=>{
 const a=await route({user:{role:'admin'},body:{question:'hello',stream:'INVALID'}});assert.equal(a.status,400);assert.equal(a.loads,0);
 const b=await route({user:{role:'admin'},body:{question:'x'.repeat(801)}});assert.equal(b.status,400);assert.equal(b.loads,0);
});
