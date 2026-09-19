/**
 * services/weakTopicService.js
 *
 * Core logic for computing student and center weak topics.
 * Implements the 70/30 Composite Scoring Model using the Sheet4 Curriculum.
 */

import { initMongo } from './mongoInit.js';
import TopicMap from '../models/TopicMap.js';
import StudentRawMarks from '../models/StudentRawMarks.js';
import StudentWeakTopics from '../models/StudentWeakTopics.js';
import CenterWeakTopics from '../models/CenterWeakTopics.js';
import {
  matchCanonicalTopic,
  getMark,
  isStudentAbsent,
} from '../utils/topicUtils.js';
import {
  computeStudentOverallWeakTopics,
  computeCenterOverallWeakTopics,
} from './overallWeakTopicService.js';

const SUBJECTS = ['PHYSICS', 'CHEMISTRY', 'MATHEMATICS', 'BOTANY', 'ZOOLOGY'];

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

export async function computeWeakTopics(testId) {
  await initMongo();

  const topicMapDoc = await TopicMap.findOne({ testId }).lean();
  if (!topicMapDoc || !topicMapDoc.topics || topicMapDoc.topics.length === 0) {
    console.warn(`[WeakTopics] No TopicMap found for testId="${testId}". Aborting computation.`);
    return { studentsProcessed: 0, studentsAbsent: 0, topicsFound: 0, smallQuestionTopics: [], centersProcessed: 0 };
  }

  // 1. Group questions by canonical topics
  const canonicalQuestionsMap = {}; // { 'Kinematics': ['Q1', 'Q2'], ... }
  const canonicalSubjectMap = {};   // { 'Kinematics': 'PHYSICS', ... }
  const allTestQuestions = new Set();
  
  for (const entry of topicMapDoc.topics) {
    for (const q of entry.questions) allTestQuestions.add(q);
    const canonical = matchCanonicalTopic(entry.topic);
    if (!canonicalQuestionsMap[canonical.name]) {
      canonicalQuestionsMap[canonical.name] = [];
      canonicalSubjectMap[canonical.name] = canonical.subject;
    }
    for (const q of entry.questions) {
      if (!canonicalQuestionsMap[canonical.name].includes(q)) {
        canonicalQuestionsMap[canonical.name].push(q);
      }
    }
  }

  const allQuestionsList = Array.from(allTestQuestions);
  const activeTopics = Object.keys(canonicalQuestionsMap);

  const allMarksDocs = await StudentRawMarks.find({ testId }).lean();
  const bulkOps = [];
  const allStudentResults = [];
  let studentsAbsent = 0;

  for (const doc of allMarksDocs) {
    const marks = marksToPlainObject(doc.marks);

    if (isStudentAbsent(marks, allQuestionsList)) {
      studentsAbsent++;
      continue;
    }

    const classification = buildEmptyTopicClassification();
    let totalScore = 0;

    for (const topicName of activeTopics) {
      const subject = canonicalSubjectMap[topicName];
      const questions = canonicalQuestionsMap[topicName];
      
      const totalQ = questions.length;
      let att = 0;
      let corr = 0;
      
      for (const q of questions) {
        const m = getMark(marks, q);
        if (m !== null) {
          totalScore += m; // Add to total score
          if (m !== 0) att++;
          if (m > 0) corr++;
        }
      }

      const AR = totalQ > 0 ? (att / totalQ) : 0;
      const Acc = att > 0 ? (corr / att) : 0;
      const CS = (0.70 * Acc) + (0.30 * AR);
      const topicObj = { topic: topicName, ar: Math.round(AR * 100), acc: Math.round(Acc * 100) };

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

    allStudentResults.push({
      studentId: doc.studentId,
      studentName: doc.studentName || '',
      centerId: doc.centerId,
      totalScore,
      ...classification
    });

    bulkOps.push({
      updateOne: {
        filter: { studentId: doc.studentId, testId },
        update: {
          $set: {
            studentName: doc.studentName || '',
            centerId: doc.centerId,
            totalScore,
            strongTopics: classification.strongTopics,
            moderateTopics: classification.moderateTopics,
            weakTopics: classification.weakTopics,
            subjectWise: classification.subjectWise,
            computedAt: new Date(),
          },
        },
        upsert: true,
      },
    });
  }

  if (bulkOps.length > 0) {
    await StudentWeakTopics.bulkWrite(bulkOps, { ordered: false });
    console.log(`[WeakTopics] Upserted ${bulkOps.length} student weak-topic docs for testId="${testId}"`);
  }

  const centersProcessed = await computeCenterWeakTopics(testId, allMarksDocs, canonicalQuestionsMap, canonicalSubjectMap, allQuestionsList);

  const allStudentIds = new Set(allStudentResults.map(r => r.studentId));
  const allCenterIds  = new Set(allStudentResults.map(r => r.centerId).filter(Boolean));

  const studentIdsArray = Array.from(allStudentIds);
  for (let i = 0; i < studentIdsArray.length; i += 25) {
    const chunk = studentIdsArray.slice(i, i + 25);
    await Promise.all(chunk.map(id => computeStudentOverallWeakTopics(id)));
  }

  const centerIdsArray = Array.from(allCenterIds);
  await Promise.all(centerIdsArray.map(id => computeCenterOverallWeakTopics(id)));

  return {
    studentsProcessed:  allStudentResults.length,
    studentsAbsent,
    topicsFound:        activeTopics.length,
    smallQuestionTopics: [], // no longer warn
    centersProcessed,
  };
}

export async function computeCenterWeakTopics(testId, allMarksDocs, canonicalQuestionsMap, canonicalSubjectMap, allQuestionsList) {
  await initMongo();

  // Group non-absent students by centerId
  const centerGroups = {};
  for (const doc of allMarksDocs) {
    const marks = marksToPlainObject(doc.marks);
    if (isStudentAbsent(marks, allQuestionsList)) continue;

    const { centerId } = doc;
    if (!centerId) continue;
    if (!centerGroups[centerId]) centerGroups[centerId] = [];
    centerGroups[centerId].push(marks);
  }

  const centerBulkOps = [];
  const activeTopics = Object.keys(canonicalQuestionsMap);

  for (const [centerId, studentsMarks] of Object.entries(centerGroups)) {
    const studentCount = studentsMarks.length;
    if (studentCount === 0) continue;

    const classification = buildEmptyTopicClassification();
    let totalScore = 0;

    for (const topicName of activeTopics) {
      const subject = canonicalSubjectMap[topicName];
      const questions = canonicalQuestionsMap[topicName];
      const totalQ = questions.length;
      
      let centerAtt = 0;
      let centerCorr = 0;
      
      for (const marks of studentsMarks) {
        for (const q of questions) {
          const m = getMark(marks, q);
          if (m !== null) {
            totalScore += m;
            if (m !== 0) centerAtt++;
            if (m > 0) centerCorr++;
          }
        }
      }

      const AR = (totalQ * studentCount) > 0 ? (centerAtt / (totalQ * studentCount)) : 0;
      const Acc = centerAtt > 0 ? (centerCorr / centerAtt) : 0;
      const CS = (0.70 * Acc) + (0.30 * AR);
      const topicObj = { topic: topicName, ar: Math.round(AR * 100), acc: Math.round(Acc * 100) };

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

    const averageScore = totalScore / studentCount;

    centerBulkOps.push({
      updateOne: {
        filter: { centerId, testId },
        update: {
          $set: {
            studentCount,
            averageScore,
            strongTopics: classification.strongTopics,
            moderateTopics: classification.moderateTopics,
            weakTopics: classification.weakTopics,
            subjectWise: classification.subjectWise,
            computedAt: new Date(),
          },
        },
        upsert: true,
      },
    });
  }

  if (centerBulkOps.length > 0) {
    await CenterWeakTopics.bulkWrite(centerBulkOps, { ordered: false });
    console.log(`[WeakTopics] Upserted ${centerBulkOps.length} center weak-topic docs for testId="${testId}"`);
  }

  return centerBulkOps.length;
}
