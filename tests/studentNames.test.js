import test from 'node:test';
import assert from 'node:assert/strict';
import { studentDisplayName, rankStudentsByTest, computeTestInsights } from '../services/analyticsService.js';

test('uploaded name header variants resolve without using parent or centre names', () => {
  for (const key of ["STUDENT'S NAME", 'Student’s Name', 'Student Name', 'studentName', 'NAME', 'name', 'Full Name']) {
    assert.equal(studentDisplayName({ [key]: '  Student One  ' }), 'Student One');
  }
  assert.equal(studentDisplayName({ "STUDENT'S NAME": ' ', NAME: 'Student Two' }), 'Student Two');
  assert.equal(studentDisplayName({ "FATHER'S NAME": 'Parent', 'CENTRE NAME': 'Centre' }), '');
});

test('ranking explorer and top/bottom lists retain names and rolls for both streams', () => {
  for (const stream of ['JEE', 'NEET']) {
    const profiles = Array.from({ length: 24 }, (_, i) => ({ ROLL_KEY: String(i + 1), NAME: `Student ${i + 1}`, centerCode: 'TEST', stream }));
    const tests = profiles.map((p, i) => ({ ROLL_KEY: p.ROLL_KEY, CMT01: i, CMT01_Physics: i }));
    const ranked = rankStudentsByTest(profiles, tests, 'CMT01');
    for (const row of [...ranked, ...ranked.slice(0, 10), ...ranked.slice(-10)]) assert.equal(row.name, `Student ${row.roll}`);
    const insights = computeTestInsights(profiles, tests, 'CMT01', ['CMT01'], { stream });
    assert.equal(insights.overallTopper.name, 'Student 24');
    assert.equal(rankStudentsByTest(profiles, [], 'CMT01')[0].name, 'Student 1');
  }
});
