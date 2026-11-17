import test from 'node:test';
import assert from 'node:assert/strict';
import { buildStudentChartData } from '../services/analyticsService.js';
test('stored test metrics remain available without a raw marks sheet', () => {
  const raw = { RMT01: 155, RMT01_Physics: 61, RMT01_Physics_Attempted: 19, RMT01_Physics_Accuracy: 84, RMT01_Total_Attempted: 55, RMT01_Total_Accuracy: 80 };
  const row = buildStudentChartData(raw, Object.keys(raw), 'JEE')[0];
  assert.equal(row.Physics_Attempted, 19);
  assert.equal(row.Physics_Accuracy, 84);
  assert.equal(row.Total_Attempted, 55);
  assert.equal(row.Total_Accuracy, 80);
});
