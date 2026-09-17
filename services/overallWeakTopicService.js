/**
 * services/overallWeakTopicService.js
 *
 * Aggregates per-test weak-topic results into a multi-test "overall" rollup
 * for both students and centers.
 * Implements the 70/30 Composite Scoring Model by summing raw attempts and correct counts
 * across all tests, then computing a single global CS.
 */

import { initMongo } from './mongoInit.js';
import StudentRawMarks from '../models/StudentRawMarks.js';
import TopicMap from '../models/TopicMap.js';
import StudentOverallWeakTopics from '../models/StudentOverallWeakTopics.js';
import CenterOverallWeakTopics from '../models/CenterOverallWeakTopics.js';
import { matchCanonicalTopic, getMark, isStudentAbsent } from '../utils/topicUtils.js';

const SUBJECTS = ['PHYSICS', 'CHEMISTRY', 'MATHEMATICS'];

function marksToPlainObject(marksField) {
  const out = {};
  if (marksField instanceof Map) {
    for (const [k, v] of marksField) out[k] = v;
  } else if (marksField && typeof marksField === 'object') {
    Object.assign(out, marksField);
  }
  return out;
}

function buildEmptyTopicClassification() {
  return {
    strongTopics: [],
    moderateTopics: [],
    weakTopics: [],
    subjectWise: {
      PHYSICS: { strong: [], moderate: [], weak: [] },
      CHEMISTRY: { strong: [], moderate: [], weak: [] },
      MATHEMATICS: { strong: [], moderate: [], weak: [] },
    }
  };
}

export async function computeStudentOverallWeakTopics(studentId) {
  await initMongo();

  const allMarksDocs = await StudentRawMarks.find({ studentId }).lean();
  if (allMarksDocs.length === 0) return;

  const centerId = allMarksDocs[0].centerId;
  const studentName = allMarksDocs[0].studentName || '';

  const testIds = allMarksDocs.map(d => d.testId);
  const topicMaps = await TopicMap.find({ testId: { $in: testIds } }).lean();
  
  const testTopicMaps = {};
  for (const tm of topicMaps) {
    const qMap = {};
    const sMap = {};
    const allQs = new Set();
    
    for (const entry of tm.topics) {
      for (const q of entry.questions) allQs.add(q);
      const canonical = matchCanonicalTopic(entry.topic);
      if (!qMap[canonical.name]) {
        qMap[canonical.name] = [];
        sMap[canonical.name] = canonical.subject;
      }
      for (const q of entry.questions) {
        if (!qMap[canonical.name].includes(q)) qMap[canonical.name].push(q);
      }
    }
    testTopicMaps[tm.testId] = { qMap, sMap, allQs: Array.from(allQs) };
  }

  // Aggregate metrics per topic across all tests
  const topicMetrics = {}; // { 'Kinematics': { att: 0, corr: 0, totalQ: 0, subject: 'PHYSICS' } }
  let totalScore = 0;
  const testsIncluded = [];

  for (const doc of allMarksDocs) {
    const tm = testTopicMaps[doc.testId];
    if (!tm) continue;

    const marks = marksToPlainObject(doc.marks);
    if (isStudentAbsent(marks, tm.allQs)) continue;
    
    testsIncluded.push(doc.testId);

    for (const [topicName, questions] of Object.entries(tm.qMap)) {
      if (!topicMetrics[topicName]) {
        topicMetrics[topicName] = { att: 0, corr: 0, totalQ: 0, subject: tm.sMap[topicName] };
      }
      topicMetrics[topicName].totalQ += questions.length;
      
      for (const q of questions) {
        const m = getMark(marks, q);
        if (m !== null) {
          totalScore += m;
          if (m !== 0) topicMetrics[topicName].att++;
          if (m > 0) topicMetrics[topicName].corr++;
        }
      }
    }
  }

  const classification = buildEmptyTopicClassification();

  for (const [topicName, metrics] of Object.entries(topicMetrics)) {
    if (metrics.totalQ === 0) continue;
    
    const AR = (metrics.att / metrics.totalQ);
    const Acc = metrics.att > 0 ? (metrics.corr / metrics.att) : 0;
    const CS = (0.70 * Acc) + (0.30 * AR);
    
    const subject = metrics.subject;

    if (CS >= 0.80 && AR >= 0.70) {
      classification.strongTopics.push(topicName);
      if (subject && classification.subjectWise[subject]) classification.subjectWise[subject].strong.push(topicName);
    } else if (CS >= 0.60 && AR >= 0.50) {
      classification.moderateTopics.push(topicName);
      if (subject && classification.subjectWise[subject]) classification.subjectWise[subject].moderate.push(topicName);
    } else {
      classification.weakTopics.push(topicName);
      if (subject && classification.subjectWise[subject]) classification.subjectWise[subject].weak.push(topicName);
    }
  }

  const finalTestsIncluded = testsIncluded.filter(t => t && t.length > 1 && t !== 'CAT4');

  await StudentOverallWeakTopics.updateOne(
    { studentId },
    {
      $set: {
        studentId,
        studentName,
        centerId,
        testsIncluded: finalTestsIncluded,
        totalTests: finalTestsIncluded.length,
        totalScore,
        strongTopics: classification.strongTopics,
        moderateTopics: classification.moderateTopics,
        weakTopics: classification.weakTopics,
        subjectWise: classification.subjectWise,
        computedAt: new Date(),
      },
    },
    { upsert: true }
  );
}

export async function computeCenterOverallWeakTopics(centerId) {
  await initMongo();

  const allMarksDocs = await StudentRawMarks.find({ centerId }).lean();
  if (allMarksDocs.length === 0) return;

  const testIds = Array.from(new Set(allMarksDocs.map(d => d.testId)));
  const topicMaps = await TopicMap.find({ testId: { $in: testIds } }).lean();
  
  const testTopicMaps = {};
  for (const tm of topicMaps) {
    const qMap = {};
    const sMap = {};
    const allQs = new Set();
    
    for (const entry of tm.topics) {
      for (const q of entry.questions) allQs.add(q);
      const canonical = matchCanonicalTopic(entry.topic);
      if (!qMap[canonical.name]) {
        qMap[canonical.name] = [];
        sMap[canonical.name] = canonical.subject;
      }
      for (const q of entry.questions) {
        if (!qMap[canonical.name].includes(q)) qMap[canonical.name].push(q);
      }
    }
    testTopicMaps[tm.testId] = { qMap, sMap, allQs: Array.from(allQs) };
  }

  // Aggregate metrics per topic across all tests
  const topicMetrics = {}; // { 'Kinematics': { att: 0, corr: 0, totalPossible: 0, subject: 'PHYSICS' } }
  let totalScore = 0;
  const testsIncluded = new Set();
  
  // Group by testId
  const testGroups = {};
  for (const doc of allMarksDocs) {
    if (!testGroups[doc.testId]) testGroups[doc.testId] = [];
    testGroups[doc.testId].push(marksToPlainObject(doc.marks));
  }
  
  let maxStudentCount = 0;

  for (const [testId, marksList] of Object.entries(testGroups)) {
    const tm = testTopicMaps[testId];
    if (!tm) continue;

    // Filter absent
    const validMarks = marksList.filter(marks => !isStudentAbsent(marks, tm.allQs));
    if (validMarks.length === 0) continue;
    
    testsIncluded.add(testId);
    if (validMarks.length > maxStudentCount) maxStudentCount = validMarks.length;

    for (const [topicName, questions] of Object.entries(tm.qMap)) {
      if (!topicMetrics[topicName]) {
        topicMetrics[topicName] = { att: 0, corr: 0, totalPossible: 0, subject: tm.sMap[topicName] };
      }
      
      const totalQ = questions.length;
      topicMetrics[topicName].totalPossible += (totalQ * validMarks.length);
      
      for (const marks of validMarks) {
        for (const q of questions) {
          const m = getMark(marks, q);
          if (m !== null) {
            totalScore += m;
            if (m !== 0) topicMetrics[topicName].att++;
            if (m > 0) topicMetrics[topicName].corr++;
          }
        }
      }
    }
  }

  const classification = buildEmptyTopicClassification();

  for (const [topicName, metrics] of Object.entries(topicMetrics)) {
    if (metrics.totalPossible === 0) continue;
    
    const AR = (metrics.att / metrics.totalPossible);
    const Acc = metrics.att > 0 ? (metrics.corr / metrics.att) : 0;
    const CS = (0.70 * Acc) + (0.30 * AR);
    
    const subject = metrics.subject;

    if (CS >= 0.80 && AR >= 0.70) {
      classification.strongTopics.push(topicName);
      if (subject && classification.subjectWise[subject]) classification.subjectWise[subject].strong.push(topicName);
    } else if (CS >= 0.60 && AR >= 0.50) {
      classification.moderateTopics.push(topicName);
      if (subject && classification.subjectWise[subject]) classification.subjectWise[subject].moderate.push(topicName);
    } else {
      classification.weakTopics.push(topicName);
      if (subject && classification.subjectWise[subject]) classification.subjectWise[subject].weak.push(topicName);
    }
  }
  
  const finalTestsIncluded = Array.from(testsIncluded).filter(t => t && t.length > 1 && t !== 'CAT4');

  await CenterOverallWeakTopics.updateOne(
    { centerId },
    {
      $set: {
        centerId,
        testsIncluded: finalTestsIncluded,
        totalTests: finalTestsIncluded.length,
        studentCount: maxStudentCount,
        averageScore: maxStudentCount > 0 ? (totalScore / maxStudentCount) : 0,
        strongTopics: classification.strongTopics,
        moderateTopics: classification.moderateTopics,
        weakTopics: classification.weakTopics,
        subjectWise: classification.subjectWise,
        computedAt: new Date(),
      },
    },
    { upsert: true }
  );
}
