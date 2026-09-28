import test from 'node:test';
import assert from 'node:assert/strict';
import { normalizeTopicSubjects } from '../utils/normalizeTopicSubjects.js';

test('saved centre and student test topics move to Chemistry without changing metrics', () => {
  for (const identity of [{ centerId: 'SKE' }, { studentId: '1' }]) {
    for (const topic of ['Ionic Equilibrium', 'Ionic Equlibrium']) {
      const ionic = { topic, ar: 35, acc: 50 };
      const doc = { ...identity, testId: 'MT02', totalScore: 100, subjectWise: {
        PHYSICS: { weak: [ionic, { topic: 'EMI', ar: 71, acc: 54 }] },
        CHEMISTRY: { weak: [{ topic: 'Chemical Bonding', ar: 41, acc: 0 }] },
      } };
      const before = JSON.stringify(doc);
      const result = normalizeTopicSubjects(doc);
      assert.equal(result.subjectWise.PHYSICS.weak.length, 1);
      assert.deepEqual(result.subjectWise.CHEMISTRY.weak[1], ionic);
      assert.equal(result.totalScore, 100);
      assert.equal(JSON.stringify(doc), before);
      assert.deepEqual(normalizeTopicSubjects(result), result);
    }
  }
  assert.equal(normalizeTopicSubjects(null), null);
});
