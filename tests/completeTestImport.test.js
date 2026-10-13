import test from 'node:test';
import assert from 'node:assert/strict';
import { validateCompleteTestImport, replacementUpdate } from '../utils/completeTestImport.js';
import { nestedToFlat } from '../utils/testColumns.js';
import { rankCentresByTest } from '../services/analyticsService.js';

const profiles = [{ ROLL_KEY: '1', centerCode: 'KNP', stream: 'JEE' }, { ROLL_KEY: '2', centerCode: 'KNP', stream: 'JEE' }];
const input = { testKey: 'MT01', stream: 'JEE', marks: [{ rollKey: '1', centerCode: 'KNP', scores: { MT01: 150, MT01_Physics: 60, MT01_Chemistry: 60, MT01_Math: 30 } }] };

test('a complete replacement excludes old test scores while preserving other tests', () => {
  const rows = validateCompleteTestImport(input, profiles);
  const docs = [{ ROLL_KEY: '1', centerCode: 'KNP', tests: { MT01: { total: 100 }, MT02: { total: 55 } } }, { ROLL_KEY: '2', centerCode: 'KNP', MT01: 50, tests: { MT01: { total: 50 }, MT02: { total: 65 } } }];
  for (const doc of docs) {
    const update = replacementUpdate(doc, 'MT01', rows.find(r => r.roll === doc.ROLL_KEY)?.scores);
    for (const key of Object.keys(update.$unset || {})) {
      if (key === 'tests.MT01') delete doc.tests.MT01;
      else delete doc[key];
    }
    if (update.$set) doc.tests.MT01 = update.$set['tests.MT01'];
  }
  const result = rankCentresByTest(profiles, docs.map(nestedToFlat), 'MT01', ['MT01']);
  assert.equal(result[0].avg, 150);
  assert.equal(result[0].tested, 1);
  assert.equal(docs[1].tests.MT02.total, 65);
  assert.equal(docs[1].MT01, undefined);
});

test('rejects duplicate, invalid, cross-test, mismatched and unknown rows before writes', () => {
  const row = input.marks[0];
  const bad = [[], [row, row], [{ ...row, rollKey: '99' }], [{ ...row, centerCode: 'DDN' }], [{ ...row, scores: { MT02: 10 } }], [{ ...row, scores: { MT01: '' } }], [{ ...row, scores: { MT01: '12oops' } }], [{ ...row, scores: { MT01: 1, MT01_Physics: 5, MT01_Chemistry: 5, MT01_Math: 5 } }]];
  for (const marks of bad) assert.throws(() => validateCompleteTestImport({ ...input, marks }, profiles));
  assert.throws(() => validateCompleteTestImport(input, [...profiles, profiles[0]]));
  assert.throws(() => validateCompleteTestImport({ ...input, testKey: 'MT01_Physics' }, profiles));
});

test('zero and negative totals are real scores, not absent students', () => {
  for (const total of [0, -5]) assert.equal(validateCompleteTestImport({ ...input, marks: [{ ...input.marks[0], scores: { MT01: total } }] }, profiles)[0].scores.total, total);
});

test('clears legacy subject keys but leaves other test and profile fields intact', () => {
  const update = replacementUpdate({ ROLL_KEY: '1', centerCode: 'KNP', MT01: 3, 'PHY MT01': 1, MT01_Math: 2, MT02: 7 }, 'MT01');
  assert.deepEqual(Object.keys(update.$unset).sort(), ['MT01', 'MT01_Math', 'PHY MT01'].sort());
});
