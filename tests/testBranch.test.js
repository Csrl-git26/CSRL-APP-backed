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
const profiles = [{ ROLL_KEY: '1', centerCode: 'A', stream: 'JEE' }, { ROLL_KEY: '2', centerCode: 'B', stream: 'JEE' }];
const columns = ['MT01','MT01_Physics','MT01_Chemistry','MT01_Math','CAT01','CAT01_Physics','CAT01_Chemistry','CAT01_Math','CAT01_Accuracy','NCT01','NCT01_Botany'];
const source = { profiles, testColumns: columns, tests: [
  { ROLL_KEY: '1', centerCode: 'A', stream: 'JEE', MT01: 120, MT01_Physics: 40, MT01_Chemistry: 40, MT01_Math: 40, CAT01: 210, CAT01_Physics: 70, CAT01_Chemistry: 70, CAT01_Math: 70, CAT01_Accuracy: 80 },
  { ROLL_KEY: '2', centerCode: 'B', stream: 'JEE', MT01: 150, MT01_Physics: 50, MT01_Chemistry: 50, MT01_Math: 50, CAT01: 180, CAT01_Physics: 60, CAT01_Chemistry: 60, CAT01_Math: 60 },
] };

test('historical JEE tests default to Main; NEET remains branchless', () => {
  for (const id of ['MT01','MT02','CMT01','FMT04']) {
    assert.equal(matchesTestBranch(id, 'MAIN', catalog), true);
    assert.equal(matchesTestBranch(id, 'ADVANCED', catalog), false);
  }
  assert.equal(matchesTestBranch('CAT01', 'ADVANCED', catalog), true);
  assert.equal(matchesTestBranch('CAT01', 'MAIN', catalog), false);
  for (const id of ['MMT01','MMT02','NCT01']) {
    assert.equal(matchesTestBranch(id, 'MAIN', catalog), true);
    assert.equal(matchesTestBranch(id, 'ADVANCED', catalog), true);
  }
});

test('filter scores and metric columns without mutating shared source; empty Advanced stays empty', () => {
  const before = JSON.stringify(source);
  const main = scopeApplicationData(source, 'MAIN', catalog);
  const advanced = scopeApplicationData(source, 'ADVANCED', catalog);
  assert.equal(main.tests[0].CAT01, undefined);
  assert.equal(main.tests[0].CAT01_Accuracy, undefined);
  assert.equal(advanced.tests[0].MT01, undefined);
  assert.equal(advanced.tests[0].CAT01_Accuracy, 80);
  assert(advanced.testColumns.includes('CAT01_Accuracy'));
  assert.equal(JSON.stringify(source), before);
  const empty = scopeApplicationData({ ...source, tests: source.tests.map(({ROLL_KEY, centerCode, MT01}) => ({ROLL_KEY, centerCode, MT01})), testColumns: ['MT01'] }, 'ADVANCED', []);
  assert.deepEqual(empty.testColumns, []);
  assert.deepEqual(empty.tests, []);
  assert.equal(empty.profiles.length, 2);
});

test('rankings and insights use the selected branch across centres', () => {
  for (const [branch, id, expectedRoll] of [['MAIN','MT01','2'], ['ADVANCED','CAT01','1']]) {
    const scoped = scopeApplicationData(source, branch, catalog);
    const ranking = rankStudentsByTest(scoped.profiles, scoped.tests, id);
    assert.equal(String(ranking[0].roll), expectedRoll);
    const centres = rankCentresByTest(scoped.profiles, scoped.tests, id, scoped.testColumns);
    assert.equal(centres.length, 2);
    const insights = computeTestInsights(scoped.profiles, scoped.tests, id, scoped.testColumns, { stream: 'JEE' });
    assert.equal(insights.rankedStudents.length, 2);
    assert.deepEqual(insights.rankedStudents.map(s => s.marks).sort((a,b) => a-b), branch === 'MAIN' ? [120,150] : [180,210]);
  }
});

test('concurrent requests isolate metadata and reuse its promise within each request', async t => {
  let reads = 0;
  t.mock.method(TestBranch, 'find', () => ({ lean: () => ({ exec: async () => { reads++; await new Promise(r => setTimeout(r, 5)); return catalog; } }) }));
  const results = await Promise.all(['MAIN','ADVANCED'].map(branch => inBranch(branch, async () => {
    const data = await filterApplicationData(source);
    const docs = await filterTestDocuments([{testId:'MT01'}, {testId:'CAT01'}]);
    return { branch: currentTestBranch(), data, docs };
  })));
  assert.equal(reads, 2);
  assert.deepEqual(results.map(r => r.docs[0].testId), ['MT01','CAT01']);
  assert.deepEqual(results.map(r => r.branch), ['MAIN','ADVANCED']);
  assert.equal(currentTestBranch(), undefined);
  assert.equal(await inBranch(undefined, () => currentTestBranch()), 'MAIN');
  assert.equal(await inBranch('ADVANCED', () => currentTestBranch(), 'POST'), undefined);
  await assert.rejects(inBranch('INVALID', () => {}), { code: 400 });
});

test('uploads reject historical reassignment and register one metadata row per test', async t => {
  const rows = [];
  t.mock.method(TestBranch, 'findOne', ({testId}) => ({ lean: async () => rows.find(r => r.testId === testId) }));
  t.mock.method(TestBranch, 'updateOne', async (_, update) => rows.push(update.$setOnInsert));
  t.mock.method(mongoose.connection, 'collection', name => ({ findOne: async query => name === 'testscores' && JSON.stringify(query).includes('tests.MT01') ? { tests: { MT01: {} } } : null }));
  await assert.rejects(registerTestBranch('MT01', {stream:'JEE',branch:'ADVANCED'}), {statusCode:409});
  await registerBulkScoreBranches([{scores:{CAT01:210,CAT01_Physics:70}}, {scores:{CAT01:180}}], {stream:'JEE',branch:'ADVANCED'});
  assert.deepEqual(rows, catalog);
  await assert.rejects(registerTestBranch('CAT01', {stream:'JEE',branch:'MAIN'}), {statusCode:409});
  await registerTestBranch('NCT02', { stream:'NEET', branch:'ADVANCED' });
  assert.equal(rows[1].branch, null);
});

test('student and centre overall topics aggregate only selected branch without overwriting shared rollups', async t => {
  const oldState = mongoose.connection.readyState;
  mongoose.connection.readyState = 1;
  t.after(() => { mongoose.connection.readyState = oldState; });
  t.mock.method(TestBranch, 'find', () => ({ lean: () => ({ exec: async () => catalog }) }));
  const raw = [
    { studentId:'1',centerId:'A',testId:'MT01',marks:{Q1:4,Q2:4,Q3:4} },
    { studentId:'1',centerId:'A',testId:'CAT01',marks:{Q1:-1,Q2:0,Q3:4} },
    { studentId:'1',centerId:'A',testId:'NCT01',marks:{Q1:4,Q2:4,Q3:4} },
  ];
  t.mock.method(StudentRawMarks, 'find', () => ({lean:async () => raw}));
  t.mock.method(TopicMap, 'find', ({testId}) => ({lean:async () => testId.$in.map(id => ({testId:id,topics:[{topic:id === 'NCT01' ? 'Cell' : 'Laws of Motion', subject:id === 'NCT01' ? 'BOTANY':'PHYSICS',questions:['Q1','Q2','Q3']}]}))}));
  for (const model of [StudentOverallWeakTopics,CenterOverallWeakTopics]) {
    t.mock.method(model, 'findOne', () => { throw new Error('Must not reuse cross-branch stored rollup'); });
    t.mock.method(model, 'updateOne', () => { throw new Error('Scoped GET must not write a rollup'); });
  }
  for (const [branch,id] of [['MAIN','MT01'],['ADVANCED','CAT01']]) {
    await inBranch(branch, async () => {
      const student = await getStudentOverallWeakTopicsForStream('1','JEE');
      const centre = await getCenterOverallWeakTopicsWithRates('A','JEE');
      assert.deepEqual(student.testsIncluded,[id]);
      assert.deepEqual(centre.testsIncluded,[id]);
      const neet = await getStudentOverallWeakTopicsForStream('1','NEET');
      assert.deepEqual(neet.testsIncluded,['NCT01']);
    });
  }
});
