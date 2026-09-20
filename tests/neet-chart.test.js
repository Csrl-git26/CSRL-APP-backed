import test from 'node:test';
import assert from 'node:assert/strict';
import { buildStudentChartData } from '../services/analyticsService.js';
import { enrichStudentChartFromRawMarks } from '../services/studentChartRawMarks.js';

test('NEET profile stream overrides legacy JEE marks metadata', () => {
  const marks = { stream: 'JEE', MT01_Physics: 40, MMT01_Physics: 100, MMT02_Botany: 140, NCT01_Zoology: 150 };
  const columns = Object.keys(marks).filter(k => k !== 'stream');
  const rows = buildStudentChartData(marks, columns, ' NEET ');
  assert.deepEqual(new Set(rows.map(r => r.name)), new Set(['MMT01', 'MMT02', 'NCT01']));
  assert.equal(rows.find(r => r.name === 'MMT02').Botany, 140);
  assert.deepEqual(buildStudentChartData(marks, columns, 'JEE').map(r => r.name), ['MT01']);
});

test('raw-only NEET tests appear, numeric string zero is not an attempt', () => {
  const rows = enrichStudentChartFromRawMarks([], [{ testId: 'MMT01', marks: { Q1: '4', Q2: '0', Q3: '-1' } }, { testId: 'MT01', marks: { Q1: 4 } }], [{ testId: 'MMT01', topics: [{ subject: 'Physics', questions: ['Q1', 'Q2'] }, { subject: 'Botany', questions: ['Q3'] }] }], 'NEET');
  assert.equal(rows.length, 1);
  assert.equal(rows[0].name, 'MMT01');
  assert.equal(rows[0].Physics, 4);
  assert.equal(rows[0].Botany, -1);
  assert.equal(rows[0].Total, 3);
  assert.equal(rows[0].Total_Attempted, 2);
  assert.equal(rows[0].Total_Accuracy, 50);
});
