import test from 'node:test';
import assert from 'node:assert/strict';
import { matchCanonicalTopic } from '../utils/topicUtils.js';
import { normalizeTopicSubjects } from '../utils/normalizeTopicSubjects.js';

test('CAT01 Mathematics topics map correctly and retain saved performance', () => {
  const topics = ['Basic Maths (Greatest Integer Function)', 'Basic Maths (Logarithm)', 'Basic Maths (Trigonometry)', 'Sets & Relation'];
  for (const topic of topics) assert.equal(matchCanonicalTopic(topic).subject, 'MATHEMATICS');
  const items = topics.map(topic => ({topic, ar:35, acc:17}));
  const source = { testId:'CAT01', subjectWise:{PHYSICS:{weak:items},MATHEMATICS:{strong:[{topic:'Matrices', ar:100, acc:100}]}}};
  const result = normalizeTopicSubjects(source);
  assert.deepEqual(result.subjectWise.PHYSICS.weak, []);
  assert.deepEqual(result.subjectWise.MATHEMATICS.weak, items);
  assert.equal(source.subjectWise.PHYSICS.weak.length, 4);
  assert.deepEqual(normalizeTopicSubjects(result), result);
  assert.equal(matchCanonicalTopic('Kinematics').subject,'PHYSICS');
});
