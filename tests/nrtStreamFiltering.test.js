import test from 'node:test';
import assert from 'node:assert/strict';
import { buildCentreChartData, buildStudentChartData } from '../services/analyticsService.js';
import { enrichStudentChartFromRawMarks } from '../services/studentChartRawMarks.js';
import { matchesTestStream } from '../utils/testStream.js';
import { matchesTestBranch, scopeApplicationData } from '../services/testBranchService.js';
const columns=['CAT01','CAT01_Physics','CAT02','CAT02_Physics','MT01','NRT01','NRT01_Physics'];
const student={ROLL_KEY:'1',CAT01:70,CAT01_Physics:20,CAT02:90,CAT02_Physics:30,MT01:80,NRT01:400,NRT01_Physics:100};
const catalog=[{testId:'CAT01',stream:'JEE',branch:'ADVANCED'},{testId:'CAT02',stream:'JEE',branch:'ADVANCED'},{testId:'NRT01',stream:'NEET',branch:null}];
test('Advanced centre and student charts exclude NRT01 even when branch-scoped data includes NEET',()=>{
 const data=scopeApplicationData({tests:[student],testColumns:columns},'ADVANCED',catalog);
 for(const rows of [buildCentreChartData(data.tests,data.testColumns,'JEE'),buildStudentChartData(data.tests[0],data.testColumns,'JEE')]){
  assert.deepEqual(rows.map(r=>r.name).sort(),['CAT01','CAT02']);
 }
});
test('NRT stays available to NEET; Main chart selection retains MT01',()=>{
 const main=scopeApplicationData({tests:[student],testColumns:columns},'MAIN',catalog);
 assert.deepEqual(buildCentreChartData(main.tests,main.testColumns,'JEE').map(r=>r.name),['MT01']);
 assert.deepEqual(buildCentreChartData([student],columns,'NEET').map(r=>r.name),['NRT01']);
 assert.deepEqual(buildStudentChartData(student,columns,'NEET').map(r=>r.name),['NRT01']);
 assert.equal(matchesTestBranch('NRT01','ADVANCED',[]),true); // NEET has no JEE branch; stream filtering is separate.
});
test('raw-mark enrichment and merge guard cannot reintroduce NRT into JEE charts',()=>{
 assert.equal(matchesTestStream('NRT01','JEE'),false);assert.equal(matchesTestStream('NRT01','NEET'),true);
 assert.equal(matchesTestStream('CAT02','JEE'),true);assert.equal(matchesTestStream('CAT02','NEET'),false);
 const raw=[{testId:'NRT01',marks:{1:4}}],maps=[{testId:'NRT01',topics:[{subject:'PHYSICS',questions:[1]}]}];
 const jee=[];enrichStudentChartFromRawMarks(jee,raw,maps,'JEE');assert.deepEqual(jee,[]);
 const neet=[];enrichStudentChartFromRawMarks(neet,raw,maps,'NEET');assert.equal(neet[0].name,'NRT01');assert.equal(neet[0].Physics,4);
});
