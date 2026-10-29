import test from 'node:test';
import assert from 'node:assert/strict';
import { qualifiesAdvanced, advancedCutoff } from '../utils/advancedQualification.js';
import { computeTestInsights } from '../services/analyticsService.js';
function result(category, total, physics, chemistry, math, branch='ADVANCED',stream='JEE') {
 const profiles=[{ROLL_KEY:'1',centerCode:'ABC',CATEGORY:category,stream}];
 const doc={ROLL_KEY:'1',CAT01:total,CAT01_Physics:physics,CAT01_Chemistry:chemistry,CAT01_Math:math};
 if(stream==='NEET') {doc.CAT01_MBBS='MBBS';doc.CAT01_Botany=30;doc.CAT01_Zoology=30;}
 return computeTestInsights(profiles,[doc],'CAT01',Object.keys(doc).filter(k=>k!=='ROLL_KEY'),{stream,branch,rollKey:'1'});
}
test('all six Advanced categories use inclusive total and subject cutoffs',()=>{
 for(const [category,total,min] of [['GEN',129.6,14.4],['EWS',118.8,14.4],['OBC',118.8,14.4],['SC',72,8.4],['ST',72,8.4],['PWD',72,8.4]]){
  const yes=result(category,total,min,min,total-2*min);
  assert.equal(yes.studentInsight.qualified,true,category);assert.equal(yes.centreRows[0].qualified,1);assert.equal(yes.centreRows[0].qualRate,100);
  assert.equal(result(category,total-0.01,min,min,total-2*min-0.01).studentInsight.qualified,false);
  for(const scores of [[min-0.01,min,total],[min,min-0.01,total],[min,total,min-0.01],[null,min,total]])assert.equal(result(category,total,...scores).studentInsight.qualified,false);
 }
});
test('missing subjects, absent totals and blank scores cannot qualify; percentages scale with configured maxima',()=>{
 assert.equal(qualifiesAdvanced(150,{Physics:20,Chemistry:20,Math:null},'GEN'),false);
 assert.equal(qualifiesAdvanced(null,{Physics:20,Chemistry:20,Math:20},'GEN'),false);
 assert.equal(qualifiesAdvanced(150,{Physics:'',Chemistry:20,Math:20},'GEN'),false);
 assert.deepEqual(advancedCutoff('GEN'),{totalPercent:36,subjectPercent:12,overallMin:129.6,subjectMin:14.4});
 assert.equal(advancedCutoff('OBC-PwD').totalPercent,20);assert.equal(advancedCutoff('').totalPercent,36);
});
test('Main retains original total-only cutoffs; NEET retains uploaded MBBS status',()=>{
 for(const [cat,total] of [['GEN',110],['EWS',90],['OBC',85],['SC',65],['ST',60],['PWD',30]]){
  assert.equal(result(cat,total,0,0,total,'MAIN').studentInsight.qualified,true);
  assert.equal(result(cat,total-1,0,0,total-1,'MAIN').studentInsight.qualified,false);
 }
 assert.equal(result('GEN',60,0,0,60,'ADVANCED','NEET').studentInsight.qualified,true);
});

test('previous 300/100 thresholds no longer qualify Advanced students',()=>{
 for(const [cat,total,sub] of [['GEN',108,12],['EWS',99,12],['OBC',99,12],['SC',60,7],['ST',60,7],['PWD',60,7]]) assert.equal(result(cat,total,sub,sub,total-2*sub).studentInsight.qualified,false);
});
