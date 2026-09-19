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
      BOTANY: { strong: [], moderate: [], weak: [] },
      ZOOLOGY: { strong: [], moderate: [], weak: [] },
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
    let isNeet = false;
    
    for (const entry of tm.topics) {
      for (const q of entry.questions) allQs.add(q);
      const canonical = matchCanonicalTopic(entry.topic);
      if (canonical.subject === 'BOTANY' || canonical.subject === 'ZOOLOGY' || canonical.name.toUpperCase().includes('BOTANY')) isNeet = true;
      if (!qMap[canonical.name]) {
        qMap[canonical.name] = [];
        sMap[canonical.name] = canonical.subject;
      }
      for (const q of entry.questions) {
        if (!qMap[canonical.name].includes(q)) qMap[canonical.name].push(q);
      }
    }
    testTopicMaps[tm.testId] = { qMap, sMap, allQs: Array.from(allQs), stream: isNeet ? 'NEET' : 'JEE' };
  }

  const streamData = {
    JEE: { topicMetrics: {}, totalScore: 0, testsIncluded: [] },
    NEET: { topicMetrics: {}, totalScore: 0, testsIncluded: [] }
  };

  for (const doc of allMarksDocs) {
    const tm = testTopicMaps[doc.testId];
    if (!tm) continue;
    const stream = tm.stream;

    const marks = marksToPlainObject(doc.marks);
    if (isStudentAbsent(marks, tm.allQs)) continue;
    
    streamData[stream].testsIncluded.push(doc.testId);

    for (const [topicName, questions] of Object.entries(tm.qMap)) {
      if (!streamData[stream].topicMetrics[topicName]) {
        streamData[stream].topicMetrics[topicName] = { att: 0, corr: 0, totalQ: 0, subject: tm.sMap[topicName] };
      }
      streamData[stream].topicMetrics[topicName].totalQ += questions.length;
      
      for (const q of questions) {
        const m = getMark(marks, q);
        if (m !== null) {
          streamData[stream].totalScore += m;
          if (m !== 0) streamData[stream].topicMetrics[topicName].att++;
          if (m > 0) streamData[stream].topicMetrics[topicName].corr++;
        }
      }
    }
  }

  for (const stream of ['JEE', 'NEET']) {
    const data = streamData[stream];
    if (data.testsIncluded.length === 0) continue;

    const classification = buildEmptyTopicClassification();

    for (const [topicName, metrics] of Object.entries(data.topicMetrics)) {
      if (metrics.totalQ === 0) continue;
      
      const AR = (metrics.att / metrics.totalQ);
      const Acc = metrics.att > 0 ? (metrics.corr / metrics.att) : 0;
      const CS = (0.70 * Acc) + (0.30 * AR);
      const topicObj = { topic: topicName, ar: Math.round(AR * 100), acc: Math.round(Acc * 100) };
      
      const subject = metrics.subject;

      if (CS >= 0.80 && AR >= 0.70) {
        classification.strongTopics.push(topicObj);
        if (subject && classification.subjectWise[subject]) classification.subjectWise[subject].strong.push(topicObj);
      } else if (CS >= 0.60 && AR >= 0.50) {
        classification.moderateTopics.push(topicObj);
        if (subject && classification.subjectWise[subject]) classification.subjectWise[subject].moderate.push(topicObj);
      } else {
        classification.weakTopics.push(topicObj);
        if (subject && classification.subjectWise[subject]) classification.subjectWise[subject].weak.push(topicObj);
      }
    }

    const finalTestsIncluded = data.testsIncluded.filter(t => t && t.length > 1 && t !== 'CAT4');

    await StudentOverallWeakTopics.updateOne(
      { studentId, stream },
      {
        $set: {
          studentId,
          stream,
          studentName,
          centerId,
          testsIncluded: finalTestsIncluded,
          totalTests: finalTestsIncluded.length,
          totalScore: data.totalScore,
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
    let isNeet = false;
    
    for (const entry of tm.topics) {
      for (const q of entry.questions) allQs.add(q);
      const canonical = matchCanonicalTopic(entry.topic);
      if (canonical.subject === 'BOTANY' || canonical.subject === 'ZOOLOGY' || canonical.name.toUpperCase().includes('BOTANY')) isNeet = true;
      if (!qMap[canonical.name]) {
        qMap[canonical.name] = [];
        sMap[canonical.name] = canonical.subject;
      }
      for (const q of entry.questions) {
        if (!qMap[canonical.name].includes(q)) qMap[canonical.name].push(q);
      }
    }
    testTopicMaps[tm.testId] = { qMap, sMap, allQs: Array.from(allQs), stream: isNeet ? 'NEET' : 'JEE' };
  }

  const streamData = {
    JEE: { topicMetrics: {}, totalScore: 0, testsIncluded: new Set(), maxStudentCount: 0 },
    NEET: { topicMetrics: {}, totalScore: 0, testsIncluded: new Set(), maxStudentCount: 0 }
  };
  
  const testGroups = {};
  for (const doc of allMarksDocs) {
    if (!testGroups[doc.testId]) testGroups[doc.testId] = [];
    testGroups[doc.testId].push(marksToPlainObject(doc.marks));
  }
  
  for (const [testId, marksList] of Object.entries(testGroups)) {
    const tm = testTopicMaps[testId];
    if (!tm) continue;
    const stream = tm.stream;

    const validMarks = marksList.filter(marks => !isStudentAbsent(marks, tm.allQs));
    if (validMarks.length === 0) continue;
    
    streamData[stream].testsIncluded.add(testId);
    if (validMarks.length > streamData[stream].maxStudentCount) streamData[stream].maxStudentCount = validMarks.length;

    for (const [topicName, questions] of Object.entries(tm.qMap)) {
      if (!streamData[stream].topicMetrics[topicName]) {
        streamData[stream].topicMetrics[topicName] = { att: 0, corr: 0, totalPossible: 0, subject: tm.sMap[topicName] };
      }
      
      const totalQ = questions.length;
      streamData[stream].topicMetrics[topicName].totalPossible += (totalQ * validMarks.length);
      
      for (const marks of validMarks) {
        for (const q of questions) {
          const m = getMark(marks, q);
          if (m !== null) {
            streamData[stream].totalScore += m;
            if (m !== 0) streamData[stream].topicMetrics[topicName].att++;
            if (m > 0) streamData[stream].topicMetrics[topicName].corr++;
          }
        }
      }
    }
  }

  for (const stream of ['JEE', 'NEET']) {
    const data = streamData[stream];
    if (data.testsIncluded.size === 0) continue;

    const classification = buildEmptyTopicClassification();
    const topicRates = [];

    for (const [topicName, metrics] of Object.entries(data.topicMetrics)) {
      if (metrics.totalPossible === 0) continue;
      
      const AR = (metrics.att / metrics.totalPossible);
      const Acc = metrics.att > 0 ? (metrics.corr / metrics.att) : 0;
      const CS = (0.70 * Acc) + (0.30 * AR);
      const topicObj = { topic: topicName, ar: Math.round(AR * 100), acc: Math.round(Acc * 100) };
      
      const subject = metrics.subject;
      topicRates.push({
        topic: topicName,
        subject,
        attempted: metrics.att,
        correct: metrics.corr,
        totalPossible: metrics.totalPossible,
        attemptPercentage: AR * 100,
        accuracyPercentage: metrics.att > 0 ? Acc * 100 : null,
      });

      if (CS >= 0.80 && AR >= 0.70) {
        classification.strongTopics.push(topicObj);
        if (subject && classification.subjectWise[subject]) classification.subjectWise[subject].strong.push(topicObj);
      } else if (CS >= 0.60 && AR >= 0.50) {
        classification.moderateTopics.push(topicObj);
        if (subject && classification.subjectWise[subject]) classification.subjectWise[subject].moderate.push(topicObj);
      } else {
        classification.weakTopics.push(topicObj);
        if (subject && classification.subjectWise[subject]) classification.subjectWise[subject].weak.push(topicObj);
      }
    }
    
    const finalTestsIncluded = Array.from(data.testsIncluded).filter(t => t && t.length > 1 && t !== 'CAT4');

    await CenterOverallWeakTopics.updateOne(
      { centerId, stream },
      {
        $set: {
          centerId,
          stream,
          testsIncluded: finalTestsIncluded,
          totalTests: finalTestsIncluded.length,
          studentCount: data.maxStudentCount,
          averageScore: data.maxStudentCount > 0 ? (data.totalScore / data.maxStudentCount) : 0,
          topicRatesVersion: 1,
          topicRates,
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
}

// Backfill legacy rollups on first access; coalesce concurrent requests per centre.
const rateBackfills = new Map();

export async function getCenterOverallWeakTopicsWithRates(centerId, stream = 'JEE') {
  await initMongo();
  let doc = await CenterOverallWeakTopics.findOne({ centerId, stream }).lean();
  if (!doc || doc.topicRatesVersion !== 1) {
    const cacheKey = `${centerId}_${stream}`;
    if (!rateBackfills.has(cacheKey)) {
      const pending = computeCenterOverallWeakTopics(centerId)
        .finally(() => rateBackfills.delete(cacheKey));
      rateBackfills.set(cacheKey, pending);
    }
    await rateBackfills.get(cacheKey);
    doc = await CenterOverallWeakTopics.findOne({ centerId, stream }).lean();
  }
  return doc;
}
