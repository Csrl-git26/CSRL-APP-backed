import test from 'node:test';
import assert from 'node:assert/strict';
import mongoose from 'mongoose';
import { TestBranch, matchesTestBranch, scopeApplicationData, filterApplicationData, filterTestDocuments, testBranchMiddleware, currentTestBranch, registerTestBranch, registerBulkScoreBranches } from '../services/testBranchService.js';
import { rankStudentsByTest, rankCentresByTest, computeTestInsights } from '../services/analyticsService.js';
import { getStudentOverallWeakTopicsForStream, getCenterOverallWeakTopicsWithRates } from '../services/overallWeakTopicService.js';
import StudentRawMarks from '../models/StudentRawMarks.js';
import TopicMap from '../models/TopicMap.js';
import StudentOverallWeakTopics from '../models/StudentOverallWeakTopics.js';
import CenterOverallWeakTopics from '../models/CenterOverallWeakTopics.js';

const catalog = [{ testId: 'CAT01', stream: 'JEE', branch: 'ADVANCED' }];
function inBranch(branch, action, method = 'GET') {
  return new Promise((resolve, reject) => testBranchMiddleware({ method, query: branch ? { branch } : {} }, {
    status(code) { return { json(body) { reject(Object.assign(new Error(body.message), { code })); } }; },
  }, () => Promise.resolve().then(action).then(resolve, reject)));
}

import { matchCanonicalTopic } from '../utils/topicUtils.js';
test('Ionic Equilibrium and historical spelling map to Chemistry', () => {
  for (const name of ['Ionic Equilibrium', 'Ionic Equlibrium', 'Q60/Ionic Equilibrium']) {
    assert.equal(matchCanonicalTopic(name).subject, 'CHEMISTRY');
    assert.equal(matchCanonicalTopic(name).name, 'Ionic Equilibrium');
  }
});
test('student and centre overall topics aggregate only selected branch without overwriting shared rollups', async t => {
  const oldState = mongoose.connection.readyState;
  mongoose.connection.readyState = 1;
  t.after(() => { mongoose.connection.readyState = oldState; });
  t.mock.method(TestBranch, 'find', () => ({ lean: () => ({ exec: async () => catalog }) }));
  const raw = [
    { studentId:'1',centerId:'A',testId:'MT01',marks:{Q1:-1,Q2:-1,Q3:-1} },
    { studentId:'1',centerId:'A',testId:'MT02',marks:{Q1:0,Q2:0,Q3:4} },
    { studentId:'1',centerId:'A',testId:'CMT01',marks:{Q1:4,Q2:4,Q3:4} },
    { studentId:'1',centerId:'A',testId:'CAT01',marks:{Q1:-1,Q2:0,Q3:4} },
    { studentId:'1',centerId:'A',testId:'NCT01',marks:{Q1:4,Q2:4,Q3:4} },
  ];
  t.mock.method(StudentRawMarks, 'find', () => ({lean:async () => raw}));
  t.mock.method(TopicMap, 'find', ({testId}) => ({lean:async () => testId.$in.map(id => ({testId:id,topics:[{topic:id === 'NCT01' ? 'Cell' : 'Ionic Equilibrium', subject:id === 'NCT01' ? 'BOTANY':'PHYSICS',questions:['Q1','Q2','Q3']}]}))}));
  for (const model of [StudentOverallWeakTopics,CenterOverallWeakTopics]) {
    t.mock.method(model, 'findOne', () => { throw new Error('Must not reuse cross-branch stored rollup'); });
    t.mock.method(model, 'updateOne', () => { throw new Error('Scoped GET must not write a rollup'); });
  }
  for (const [branch,id] of [['MAIN','CMT01'],['ADVANCED','CAT01']]) {
    await inBranch(branch, async () => {
      const student = await getStudentOverallWeakTopicsForStream('1','JEE');
      const centre = await getCenterOverallWeakTopicsWithRates('A','JEE');
      assert.deepEqual(student.testsIncluded,[id]);
      assert.equal(student.subjectWise.PHYSICS.strong.length + student.subjectWise.PHYSICS.moderate.length + student.subjectWise.PHYSICS.weak.length, 0);
      assert.equal(centre.topicRates[0].subject, 'CHEMISTRY');
      assert.equal(centre.topicRates[0].topic, 'Ionic Equilibrium');
      assert.deepEqual(centre.testsIncluded,[id]);
      if (branch === 'MAIN') {
        assert.equal(student.totalTests, 1);
        assert.equal(centre.totalTests, 1);
        assert.equal(student.totalScore, 12);
        assert.equal(centre.averageScore, 12);
        assert.equal(student.strongTopics[0].ar, 100);
        assert.equal(student.strongTopics[0].acc, 100);
        assert.equal(centre.topicRates[0].totalPossible, 3);
        assert.equal(centre.topicRates[0].attemptPercentage, 100);
        assert.equal(centre.topicRates[0].accuracyPercentage, 100);
      }
      const neetCentre = await getCenterOverallWeakTopicsWithRates('A','NEET');
      assert.deepEqual(neetCentre.testsIncluded,['NCT01']);
      const neet = await getStudentOverallWeakTopicsForStream('1','NEET');
      assert.deepEqual(neet.testsIncluded,['NCT01']);
    });
  }
  raw.splice(raw.findIndex(doc => doc.testId === 'CMT01'), 1);
  await inBranch('MAIN', async () => {
    assert.equal(await getStudentOverallWeakTopicsForStream('1', 'JEE'), undefined);
    assert.equal(await getCenterOverallWeakTopicsWithRates('A', 'JEE'), undefined);
  });
});

