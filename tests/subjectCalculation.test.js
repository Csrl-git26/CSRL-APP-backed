import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { parseTestSheet, parseTopicMapSheet } from '../services/csvParserService.js';
import { normalizeTestTopicMap, applyVerifiedRawScores } from '../utils/testSubjectMapping.js';
import { normalizeTopicSubjects } from '../utils/normalizeTopicSubjects.js';
import { parseTestColumn } from '../utils/testColumns.js';
import { buildCentreChartData, computeTestInsights, rankStudentsByTest, rankCentresByTest, absentCount } from '../services/analyticsService.js';
import { enrichStudentChartFromRawMarks } from '../services/studentChartRawMarks.js';
import TopicMap from '../models/TopicMap.js';

test('historical NCT01 maps are corrected through actual lean find and findOne queries', async t => {
  const old = { testId: 'NCT01', topics: [{ topic: 'Biomolecules', subject: 'Chemistry', questions: ['Q137', 'Q180'] }] };
  t.mock.method(TopicMap.collection, 'find', () => ({ toArray: async () => [structuredClone(old)] }));
  t.mock.method(TopicMap.collection, 'findOne', async () => structuredClone(old));
  for (const doc of [(await TopicMap.find({}).lean())[0], await TopicMap.findOne({}).lean()]) {
    assert.equal(doc.topics[0].subject, 'ZOOLOGY');
    assert.equal(doc.topics[0].questionCount, 2);
  }
  assert.equal(old.topics[0].subject, 'Chemistry');
  assert.equal(normalizeTestTopicMap({ ...old, testId: 'CMT01' }).topics[0].subject, 'CHEMISTRY');
});

test('saved individual topic classifications move NCT01 Biomolecules only', () => {
  const doc = { testId: 'NCT01', subjectWise: { CHEMISTRY: { strong: [{ topic: 'Biomolecules', ar: 80, acc: 90 }] } } };
  const result = normalizeTopicSubjects(doc);
  assert.equal(result.subjectWise.CHEMISTRY.strong.length, 0);
  assert.deepEqual(result.subjectWise.ZOOLOGY.strong[0], { topic: 'Biomolecules', ar: 80, acc: 90 });
  assert.equal(normalizeTopicSubjects({ ...doc, testId: 'CMT01' }).subjectWise.CHEMISTRY.strong.length, 1);
});

test('shared topic names require explicit subjects and never pollute later imports', () => {
  const explicit = Buffer.from('Question,Topic,Subject\nQ1,Biomolecules,Chemistry\nQ2,Biomolecules,Zoology');
  const parsed = parseTopicMapSheet(explicit);
  assert.equal(Object.keys(parsed.topicsWithQuestions).length, 2);
  assert.deepEqual(parsed.questionSubjectMap, { Q1: 'Chemistry', Q2: 'Zoology' });
  assert.equal(parseTopicMapSheet(Buffer.from('Question,Topic\nQ1,Zoology: Biomolecules')).questionTopicMap.Q1, 'Biomolecules');
  assert.equal(parseTopicMapSheet(Buffer.from('Question,Topic,Subject\nQ137,Biomolecules,Chemistry'), { testId: 'NCT01' }).questionSubjectMap.Q137, 'Zoology');
  assert.throws(() => parseTopicMapSheet(Buffer.from('Question,Topic\nQ1,Biomolecules')), /validation failed/);
  const maths = parseTopicMapSheet(Buffer.from('Question,Topic\nQ1,Basic Maths (Logarithm)\nQ2,Sets & Relation\nQ3,Ionic Equlibrium'));
  assert.deepEqual(maths.questionSubjectMap, { Q1: 'Mathematics', Q2: 'Mathematics', Q3: 'Chemistry' });
});

test('centre averages retain zero and negative marks, including sums that return to zero', () => {
  const rows = [0, 10].map(v => ({ CMT01: v, CMT01_Physics: v }));
  assert.equal(buildCentreChartData(rows, ['CMT01', 'CMT01_Physics'], 'JEE')[0].Physics, 5);
  const cancelling = [-10, 10, 30].map(v => ({ CMT01: v, CMT01_Physics: v }));
  assert.equal(buildCentreChartData(cancelling, ['CMT01', 'CMT01_Physics'], 'JEE')[0].Physics, 10);
});

test('rankings, subject leaders and insights never borrow other-test scores or clamp negatives', () => {
  const profiles = ['a','b','c'].map(ROLL_KEY => ({ ROLL_KEY, centerCode: ROLL_KEY, stream: 'JEE' }));
  const tests = [
    { ROLL_KEY: 'a', CMT01: -7, CMT01_Physics: -7, MT01_Math: 99 },
    { ROLL_KEY: 'b', CMT01: 0, CMT01_Physics: 0 },
    { ROLL_KEY: 'c', MT01_Physics: 80, CMT01_Physics: '' }
  ];
  const insights = computeTestInsights(profiles, tests, 'CMT01', [], { stream: 'JEE' });
  assert.equal(insights.centreRows.find(c => c.code === 'a').subjectAvgs.Physics, -7);
  assert.equal(insights.centreRows.some(c => c.code === 'c'), false);
  assert.equal(insights.subjects.includes('Math'), false);
  assert.deepEqual(rankStudentsByTest(profiles, tests, 'CMT01').map(s => s.marks), [0, -7, 'Absent']);
  assert.equal(absentCount(profiles, tests, 'CMT01'), 1);
  assert.equal(rankCentresByTest(profiles, tests, 'CMT01', []).length, 2);
  const onlyMath = [{ ROLL_KEY: 'a', CMT01_Mathematics: -3, CMT010_Physics: 100, CMT01_Physics_Accuracy: 90 }];
  assert.equal(rankStudentsByTest(profiles.slice(0,1), onlyMath, 'CMT01')[0].marks, -3);
  assert.equal(onlyMath[0].CMT01, undefined);
});

test('NCT01 supplied CSV: every student and centre reconciles to independent 45-question sums', { skip: !process.env.NCT01_AUDIT_CSV }, () => {
  const parsed = parseTestSheet(fs.readFileSync(process.env.NCT01_AUDIT_CSV), { testId: 'NCT01' });
  assert.equal(parsed.students.length, 463);
  const subjects = ['Physics', 'Chemistry', 'Botany', 'Zoology'];
  const profiles = parsed.students.map(s => ({ ROLL_KEY: s.studentId, centerCode: s.centerId, stream: 'NEET' }));
  const raw = parsed.students.map(s => ({ ...s, testId: 'NCT01' }));
  const data = applyVerifiedRawScores({ profiles, tests: profiles.map(p => ({ ...p })), testColumns: [] }, raw, parseTestColumn);
  const maps = [{ testId: 'NCT01', topics: Object.values(parsed.topicsWithQuestions) }];
  const independent = new Map();
  parsed.students.forEach((s, i) => {
    const expected = subjects.map((_, sub) => Array.from({ length: 45 }, (_, q) => Number(s.marks[`Q${sub*45+q+1}`])).reduce((a,b) => a+b, 0));
    subjects.forEach((sub, j) => assert.equal(data.tests[i][`NCT01_${sub}`], expected[j]));
    assert.equal(data.tests[i].NCT01, expected.reduce((a,b) => a+b, 0));
    const chart = enrichStudentChartFromRawMarks([], [raw[i]], maps, 'NEET')[0];
    subjects.forEach((sub, j) => assert.equal(chart[sub], expected[j]));
    if (!independent.has(s.centerId)) independent.set(s.centerId, []);
    independent.get(s.centerId).push(expected);
  });
  const insights = computeTestInsights(profiles, data.tests, 'NCT01', data.testColumns, { stream: 'NEET' });
  assert.equal(insights.centreRows.length, 12);
  for (const centre of insights.centreRows) {
    const rows = independent.get(centre.code);
    assert.equal(centre.appeared, rows.length);
    subjects.forEach((sub, i) => assert.equal(centre.subjectAvgs[sub], Math.round(rows.reduce((sum,row) => sum+row[i], 0)/rows.length*100)/100));
  }
  const glt = insights.centreRows.find(c => c.code === 'GLT');
  assert.deepEqual(glt.subjectAvgs, { Physics:52.37, Chemistry:72.73, Botany:120.43, Zoology:115.83 });
  assert.equal(glt.totalAvg, 361.37);
  assert.equal(glt.rank, 4);
  assert.equal([...insights.centreRows].sort((a,b) => b.subjectAvgs.Zoology-a.subjectAvgs.Zoology).findIndex(c => c.code === 'GLT')+1, 6);
});
