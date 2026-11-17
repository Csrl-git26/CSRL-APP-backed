import test from 'node:test';
import assert from 'node:assert/strict';
import { sameStudentMetricCentre } from '../utils/studentMetricCentre.js';
import { enrichStudentChartFromRawMarks } from '../services/studentChartRawMarks.js';
test('batch metrics accept import centre aliases and reject different centres', () => {
  for (const [stored, displayed] of [['OIL_INDIA','JDH'],['OIL INDIA','JDH'],['GAIL','KNP'],['DEL','DEL']]) {
    assert.equal(sameStudentMetricCentre(stored, displayed), true);
    const row = {name:'RMT01'};
    const record = {testId:'RMT01',centerId:stored,marks:{1:4,2:-1,3:0}};
    if (sameStudentMetricCentre(record.centerId, displayed)) enrichStudentChartFromRawMarks([row],[record],[{testId:'RMT01',topics:[{subject:'Physics',questions:[1,2,3]}]}],'JEE');
    assert.equal(row.Physics_Attempted,2);
    assert.equal(row.Physics_Accuracy,50);
    assert.equal(row.Total_Attempted,2);
    assert.equal(row.Total_Accuracy,50);
  }
  assert.equal(sameStudentMetricCentre('OIL_INDIA','KNP'),false);
  assert.equal(sameStudentMetricCentre('', ''),false);
});

test('NEET Mumbai import alias matches MUMM without merging JEE centres', () => {
  assert.equal(sameStudentMetricCentre('MUM', 'MUMM', 'NEET'), true);
  assert.equal(sameStudentMetricCentre('MUM', 'MUMM', 'JEE'), false);
  assert.equal(sameStudentMetricCentre('MUM', 'MUMM'), false);
  const row = { name: 'NRT01' };
  const record = {testId:'NRT01',centerId:'MUM',marks:{1:4,2:-1}};
  if (sameStudentMetricCentre(record.centerId, 'MUMM', 'NEET')) enrichStudentChartFromRawMarks([row],[record],[{testId:'NRT01',topics:[{subject:'Physics',questions:[1,2]}]}],'NEET');
  assert.equal(row.Physics_Attempted,2);
  assert.equal(row.Physics_Accuracy,50);
  assert.equal(row.Total_Attempted,2);
});
