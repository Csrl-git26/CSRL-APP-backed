import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import { readFileSync } from 'node:fs';

test('missing NEET summary is recovered read-only using test prefix and explicit subjects', async () => {
  let writes = 0;
  const raw = [{ testId: 'MMT01', centerId: 'TEST', marks: { Q1: 4, Q2: -1 } }, { testId: 'MT01', centerId: 'TEST', marks: { Q1: 4 } }];
  const maps = [{ testId: 'MMT01', topics: [{ topic: 'Kinematics', subject: 'Physics', questions: ['Q1'] }, { topic: 'Biomolecules', subject: 'Zoology', questions: ['Q2'] }] }, { testId: 'MT01', topics: [{ topic: 'Kinematics', subject: 'Physics', questions: ['Q1'] }] }];
  const ctx = vm.createContext({ Map, Set, Date, initMongo: async () => {},
    StudentRawMarks: { find: () => ({ lean: async () => raw }) },
    TopicMap: { find: () => ({ lean: async () => maps }) },
    StudentOverallWeakTopics: { findOne: () => ({ lean: async () => null }), updateOne: async () => { writes++; } },
    CenterOverallWeakTopics: {},
  });
  vm.runInContext(readFileSync(new URL('../utils/topicUtils.js', import.meta.url), 'utf8').replaceAll('export ', ''), ctx);
  vm.runInContext(readFileSync(new URL('../services/overallWeakTopicService.js', import.meta.url), 'utf8').replace(/^import .*;\n/gm, '').replaceAll('export ', ''), ctx);
  const doc = await ctx.getStudentOverallWeakTopicsForStream('2722018', 'NEET');
  assert.equal(doc.stream, 'NEET');
  assert.deepEqual(Array.from(doc.testsIncluded), ['MMT01']);
  assert.equal(doc.subjectWise.ZOOLOGY.weak[0].topic, 'Biomolecules');
  assert.equal(doc.subjectWise.PHYSICS.strong[0].topic, 'Kinematics');
  assert.equal(doc.subjectWise.CHEMISTRY.weak.length, 0);
  assert.equal(writes, 0);
});
