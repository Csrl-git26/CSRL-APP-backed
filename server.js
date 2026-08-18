import './bootstrap-env.js';
import express from 'express';
import cors from 'cors';
import jwt from 'jsonwebtoken';
import multer from 'multer';
import { isMongoReady, initMongo } from './services/mongoInit.js';
import TopicMap from './models/TopicMap.js';
import StudentRawMarks from './models/StudentRawMarks.js';
import StudentWeakTopics from './models/StudentWeakTopics.js';
import CenterWeakTopics from './models/CenterWeakTopics.js';
import StudentOverallWeakTopics from './models/StudentOverallWeakTopics.js';
import CenterOverallWeakTopics from './models/CenterOverallWeakTopics.js';
import SyllabusTopics from './models/SyllabusTopics.js';
import TestScore from './models/TestScore.js';
import PastYearData from './models/PastYearData.js';
import { seedTopics } from './seedTopics.js';
import { parseTestSheet, buildTopicSubjectLookup } from './services/csvParserService.js';
import { computeWeakTopics } from './services/weakTopicService.js';
import {
  isDbEnabled,
  upsertProfileDoc,
  deleteStudentDocs,
  upsertTestDoc,
  loadApplicationData,
  loadCenterApplicationData,
  sliceCenterFromGlobal,
  getReadCacheStatus,
  invalidateDataCache,
} from './services/dbService.js';
import { flatToNested, parseTestColumn } from './utils/testColumns.js';
import {
  computeOverview,
  rankStudentsByTest,
  absentCount,
  rankCentresByTest,
  computeWeakSubjectAnalysis,
  subjectAverages,
  subjectAveragesForTest,
  computeStudentWeakSubject,
  computeTestInsights,
  buildCentreChartData,
} from './services/analyticsService.js';
import { CENTERS_CONFIG, ADMIN_CREDENTIALS } from './config/centers.js';

const app = express();
const PORT = process.env.PORT || 5001;
const JWT_SECRET = process.env.JWT_SECRET || 'csrl_super_secret_key_2026';

app.use(cors({ origin: '*' }));
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb', extended: true }));

app.get('/api/health', async (_req, res) => {
  const global = await loadApplicationData();
  res.json({
    ok: true,
    mongoReady: isMongoReady(),
    dbEnabled: isDbEnabled(),
    readCache: getReadCacheStatus(),
    counts: {
      profiles: global.profiles.length,
      tests: global.tests.length,
      testColumns: global.testColumns.length,
    },
  });
});

// ── Profile helpers ────────────────────────────────────────────────────────────

function normalizeRollKey(v) {
  return String(v ?? '').trim().replace(/\.0+$/, '').toUpperCase();
}

function normalizeCenterCode(v) {
  return String(v ?? '').trim().toUpperCase();
}

function findProfileIndex(globalData, rollKey, centerCode) {
  const normalizedRoll = normalizeRollKey(rollKey);
  const normalizedCenter = normalizeCenterCode(centerCode);

  if (centerCode) {
    return globalData.profiles.findIndex(
      (p) =>
        normalizeRollKey(p.ROLL_KEY) === normalizedRoll &&
        normalizeCenterCode(p.centerCode) === normalizedCenter
    );
  }
  const matches = globalData.profiles.filter((p) => normalizeRollKey(p.ROLL_KEY) === normalizedRoll);
  if (matches.length > 1) return -2;
  return globalData.profiles.findIndex((p) => normalizeRollKey(p.ROLL_KEY) === normalizedRoll);
}

function findProfile(globalData, rollKey, centerCode) {
  const idx = findProfileIndex(globalData, rollKey, centerCode);
  if (idx < 0) return null;
  return globalData.profiles[idx];
}

// ── Auth ───────────────────────────────────────────────────────────────────────

app.post('/api/auth/login', async (req, res) => {
  const { role, id, password } = req.body;

  if (role === 'admin') {
    if (id === ADMIN_CREDENTIALS.username && password === ADMIN_CREDENTIALS.password) {
      const token = jwt.sign({ role: 'admin', id: 'admin' }, JWT_SECRET, { expiresIn: '12h' });
      return res.json({ success: true, token, role: 'admin', id: 'admin', name: 'CSRL Admin' });
    }
  } else if (role === 'centre') {
    if (id === 'centre' && password === 'centre123') {
      const token = jwt.sign({ role: 'centre', id: 'centre' }, JWT_SECRET, { expiresIn: '12h' });
      return res.json({ success: true, token, role: 'centre', id: 'centre', name: 'Centre Dashboard' });
    }
  } else if (role === 'bog') {
    if (id === 'BOG' && password === 'Csrl@123') {
      const token = jwt.sign({ role: 'bog', id: 'bog' }, JWT_SECRET, { expiresIn: '12h' });
      return res.json({ success: true, token, role: 'bog', id: 'bog', name: 'BOG Dashboard' });
    }
  } else if (role === 'student') {
    const globalData = await loadApplicationData();
    const normalizedId = normalizeRollKey(id);
    const student = globalData.profiles.find(
      (p) => normalizeRollKey(p.ROLL_KEY) === normalizedId || normalizeRollKey(p['ROLL NO.']) === normalizedId
    );
    if (student) {
      const token = jwt.sign(
        { role: 'student', id: student.ROLL_KEY, centerCode: student.centerCode },
        JWT_SECRET,
        { expiresIn: '12h' }
      );
      return res.json({
        success: true,
        token,
        role: 'student',
        id: student.ROLL_KEY,
        name: student["STUDENT'S NAME"],
        centerCode: student.centerCode,
        stream: student.stream || 'JEE',
      });
    }
  }

  return res.status(401).json({ success: false, message: 'Invalid credentials' });
});

// ── Auth Middleware ────────────────────────────────────────────────────────────

function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];
  if (!token) return res.sendStatus(401);
  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
}

function requireAdmin(req, res, next) {
  if (req.user.role !== 'admin') return res.status(403).json({ message: 'Admin only' });
  next();
}

// ── Data Read Routes ───────────────────────────────────────────────────────────

app.get('/api/data/global', authenticateToken, async (req, res) => {
  if (req.user.role !== 'admin') return res.status(403).json({ message: 'Forbidden' });
  res.json(await loadApplicationData());
});

app.get('/api/data/center', authenticateToken, async (req, res) => {
  if (req.user.role !== 'centre' && req.user.role !== 'admin' && req.user.role !== 'bog') {
    return res.status(403).json({ message: 'Forbidden' });
  }
  const centerCode = req.query.centerCode || req.user.id;
  res.json(await loadCenterApplicationData(centerCode));
});

app.get('/api/data/centers', authenticateToken, async (req, res) => {
  if (req.user.role !== 'centre' && req.user.role !== 'admin' && req.user.role !== 'bog') {
    return res.status(403).json({ message: 'Forbidden' });
  }
  const global = await loadApplicationData();
  const centerMap = {};
  
  global.profiles.forEach((p) => {
    if (!p.centerCode) return;
    const code = p.centerCode.toUpperCase();
    const sponsor = p.SPONSOR || '';
    
    if (!centerMap[code]) {
      centerMap[code] = { code, name: code, sponsor: '' };
    }
    
    if (sponsor) centerMap[code].sponsor = sponsor;
    const currentSponsor = centerMap[code].sponsor;
    const currentCenterCode = p['CENTRE CODE'] || code;
    
    centerMap[code].name = currentSponsor ? `${currentSponsor}-${currentCenterCode}` : currentCenterCode;
  });


  res.json(Object.values(centerMap));
});

app.get('/api/data/student', authenticateToken, async (req, res) => {
  if (req.user.role !== 'student') return res.status(403).json({ message: 'Forbidden' });
  const centerData = await loadCenterApplicationData(req.user.centerCode);
  res.json({
    profiles: centerData.profiles.filter((p) => p.ROLL_KEY === req.user.id),
    tests: centerData.tests.filter((t) => t.ROLL_KEY === req.user.id),
    testColumns: centerData.testColumns,
  });
});

// ── Analytics Routes ───────────────────────────────────────────────────────────

/**
 * GET /api/analytics/overview?centerCode=
 * Returns high-level KPIs. Scoped to a centre if centerCode is provided.
 */
app.get('/api/analytics/overview', authenticateToken, async (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  const { centerCode } = req.query;
  let source;
  if (centerCode) {
    source = await loadCenterApplicationData(centerCode);
  } else {
    source = await loadApplicationData();
  }
  const result = computeOverview(source.profiles, source.tests, source.testColumns);
  res.json(result);
});

/**
 * GET /api/analytics/rankings?testKey=&centerCode=&limit=30&order=desc
 * Rank students by a test column.
 * order=asc returns bottom (lowest scores first).
 */
app.get('/api/analytics/rankings', authenticateToken, async (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  const { testKey, centerCode, limit = '30', order = 'desc' } = req.query;
  if (!testKey) return res.status(400).json({ message: 'testKey is required' });

  const source = centerCode ? await loadCenterApplicationData(centerCode) : await loadApplicationData();
  let ranked = rankStudentsByTest(source.profiles, source.tests, testKey);
  const absent = absentCount(source.profiles, source.tests, testKey);

  if (order === 'asc') ranked = ranked.filter(s => s.marks !== 'Absent').reverse();

  const n = Math.min(parseInt(limit, 10) || 30, ranked.length);
  res.json({
    ranked: ranked.slice(0, n),
    total: ranked.length,
    absentCount: absent,
    testKey,
  });
});

/**
 * GET /api/analytics/centre-leaderboard?testKey=
 * Rank all centres by average score for the given test column.
 */
app.get('/api/analytics/centre-leaderboard', authenticateToken, async (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  const { testKey } = req.query;
  if (!testKey) return res.status(400).json({ message: 'testKey is required' });

  const global = await loadApplicationData();
  let result = rankCentresByTest(global.profiles, global.tests, testKey, global.testColumns);
  
  const insights = computeTestInsights(global.profiles, global.tests, testKey, global.testColumns);

  try {
    const weakData = await CenterWeakTopics.find({ testId: testKey }).lean();
    
    result = result.map(centre => {
      const centerAccData = weakData.find(d => d.centerId === centre.code);
      let accuracyWeakSubject = 'None';
      
      if (centerAccData && centerAccData.weakSubjects) {
        let highestPercent = 0;
        let weakestSub = null;
        let isMedium = false;
        
        Object.keys(centerAccData.weakSubjects).forEach(sub => {
          const strong = centerAccData.weakSubjects[sub]?.strongWeak;
          if (strong && strong.length > 0 && strong[0].percentage > highestPercent) {
            highestPercent = strong[0].percentage;
            weakestSub = sub;
            isMedium = false;
          }
        });
        
        if (!weakestSub) {
          Object.keys(centerAccData.weakSubjects).forEach(sub => {
            const medium = centerAccData.weakSubjects[sub]?.mediumWeak;
            if (medium && medium.length > 0 && medium[0].percentage > highestPercent) {
              highestPercent = medium[0].percentage;
              weakestSub = sub;
              isMedium = true;
            }
          });
        }
        
        if (weakestSub) {
          accuracyWeakSubject = isMedium ? `${weakestSub} (Medium)` : weakestSub;
        }
      }
      
      const insightRow = insights.centreRows.find(r => r.code === centre.code);
      const qualRate = insightRow ? insightRow.qualRate : 0;
      const qualifiedCount = insightRow ? insightRow.qualified : 0;
      
      const notQualBySub = {};
      if (insights.subjects) {
         insights.subjects.forEach(subj => {
            if (insights.notQualifiedBySubject[subj] && insights.notQualifiedBySubject[subj][centre.code]) {
               notQualBySub[subj] = insights.notQualifiedBySubject[subj][centre.code];
            }
         });
      }
      
      return { ...centre, accuracyWeakSubject, qualRate, qualifiedCount, notQualBySub };
    });
  } catch (error) {
    console.error('Error fetching accuracy weak topics for leaderboard:', error);
  }

  res.json(result);
});

/**
 * GET /api/analytics/subject-averages?centerCode=&testKey=
 * Per-subject averages (weakest first). Scoped to a centre if centerCode provided.
 * If testKey is set, only that test’s subject columns are included (not all tests).
 */
app.get('/api/analytics/subject-averages', authenticateToken, async (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  const { centerCode, testKey } = req.query;
  const source = centerCode ? await loadCenterApplicationData(centerCode) : await loadApplicationData();
  const result = testKey
    ? subjectAveragesForTest(source.tests, source.testColumns, testKey)
    : subjectAverages(source.tests, source.testColumns);
  res.json(result);
});

/**
 * GET /api/analytics/test-insights?testKey=&rollKey=
 * CAT-style analysis (marks-based). Uses global data. Optional rollKey for student card.
 */
app.get('/api/analytics/test-insights', authenticateToken, async (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  const { testKey, rollKey } = req.query;
  if (!testKey) return res.status(400).json({ message: 'testKey is required' });

  const global = await loadApplicationData();
  const result = computeTestInsights(global.profiles, global.tests, testKey, global.testColumns, {
    rollKey: rollKey || undefined,
  });
  res.json(result);
});

/**
 * GET /api/analytics/student-chart?rollKey=&centerCode=
 * Chart-ready performance data for a single student.
 */
app.get('/api/analytics/student-chart', async (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');

  const { rollKey, centerCode } = req.query;
  if (!rollKey) return res.status(400).json({ message: 'rollKey is required' });

  const source = centerCode ? await loadCenterApplicationData(centerCode) : await loadApplicationData();
  const testDoc = source.tests.find((t) => t.ROLL_KEY === rollKey) || {};
  const chartData = buildStudentChartData(testDoc, source.testColumns);
  const weakSubj = computeStudentWeakSubject(testDoc, source.testColumns);

  try {
    const rawMarks = await StudentRawMarks.find({ studentId: rollKey }).lean();
    if (rawMarks && rawMarks.length > 0) {
      const topicMaps = await TopicMap.find({ testId: { $in: rawMarks.map(m => m.testId) } }).lean();
      
      chartData.forEach(row => {
        const normRowName = row.name.replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
        const rawMarkDoc = rawMarks.find(m => m.testId && m.testId.replace(/[^a-zA-Z0-9]/g, '').toUpperCase() === normRowName);
        
        if (rawMarkDoc && rawMarkDoc.marks) {
          const tMap = topicMaps.find(t => t.testId === rawMarkDoc.testId);
          if (tMap) {
            const qToSub = {};
            (tMap.topics || []).forEach(t => {
              (t.questions || []).forEach(q => {
                qToSub[q] = t.subject;
              });
            });
            
            const metrics = {};
            let totalAttempted = 0;
            let totalCorrect = 0;
            
            let marksEntries = [];
            if (rawMarkDoc.marks instanceof Map) {
              marksEntries = Array.from(rawMarkDoc.marks.entries());
            } else if (typeof rawMarkDoc.marks === 'object' && rawMarkDoc.marks !== null) {
              marksEntries = Object.entries(rawMarkDoc.marks);
            }
            
            marksEntries.forEach(([q, mark]) => {
              const sub = qToSub[q];
              if (!sub) return;
              if (!metrics[sub]) metrics[sub] = { attempted: 0, correct: 0 };
              
              if (mark !== undefined && mark !== null) {
                metrics[sub].attempted++;
                totalAttempted++;
                if (Number(mark) > 0) {
                  metrics[sub].correct++;
                  totalCorrect++;
                }
              }
            });
            
            Object.keys(metrics).forEach(sub => {
              const outSub = sub === 'Mathematics' ? 'Math' : sub;
              row[`${outSub}_Attempted`] = metrics[sub].attempted;
              row[`${outSub}_Correct`] = metrics[sub].correct;
              if (metrics[sub].attempted > 0) {
                row[`${outSub}_Accuracy`] = Math.round((metrics[sub].correct / metrics[sub].attempted) * 100);
              } else {
                row[`${outSub}_Accuracy`] = 0;
              }
            });
            
            row['Total_Attempted'] = totalAttempted;
            row['Total_Correct'] = totalCorrect;
            row['Total_Accuracy'] = totalAttempted > 0 ? Math.round((totalCorrect / totalAttempted) * 100) : 0;
            row['FALLBACK_DEBUG'] = 'RAN';
          }
        }
      });
    }

    const weakTopics = await StudentWeakTopics.find({ studentId: rollKey }).lean();
    const weakMap = {};
    for (const wt of weakTopics) {
      const normKey = (wt.testId || '').replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
      if (!weakMap[normKey]) {
        weakMap[normKey] = {
          attempted: 0,
          correct: 0,
          wrong: 0,
          totalQuestions: 0,
          subjectMetrics: {
            Physics: { attempted: 0, correct: 0, wrong: 0 },
            Chemistry: { attempted: 0, correct: 0, wrong: 0 },
            Mathematics: { attempted: 0, correct: 0, wrong: 0 },
            Biology: { attempted: 0, correct: 0, wrong: 0 },
          }
        };
      }
      
      const target = weakMap[normKey];
      target.attempted += (wt.attempted || 0);
      target.correct += (wt.correct || 0);
      target.wrong += (wt.wrong || 0);
      
      if (wt.subjectMetrics) {
        ['Physics', 'Chemistry', 'Mathematics', 'Biology'].forEach(sub => {
          if (wt.subjectMetrics[sub]) {
            target.subjectMetrics[sub].attempted += (wt.subjectMetrics[sub].attempted || 0);
            target.subjectMetrics[sub].correct += (wt.subjectMetrics[sub].correct || 0);
            target.subjectMetrics[sub].wrong += (wt.subjectMetrics[sub].wrong || 0);
          }
        });
      }
    }

    let enrichedChartData = [...chartData];

    // Add any tests from weakTopics that are NOT in chartData (e.g. if they only uploaded Weak Topics and not Flat Marks)
    for (const wt of weakTopics) {
      const normKey = (wt.testId || '').replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
      if (!enrichedChartData.some(r => (r.name || '').replace(/[^a-zA-Z0-9]/g, '').toUpperCase() === normKey)) {
        enrichedChartData.push({
          name: wt.testId,
          Physics: null, Chemistry: null, Math: null, Biology: null, Total: null
        });
      }
    }

    // Sort again just in case we appended tests
    enrichedChartData.sort((a, b) => (a.name || '').localeCompare(b.name || '', undefined, { numeric: true }));

    const finalChartData = enrichedChartData.map((row) => {
      const normRowName = (row.name || '').replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
      
      // Calculate global rankings for this test
      ['Total', 'Physics', 'Chemistry', 'Math', 'Biology'].forEach((sub) => {
        const testKey = sub === 'Total' ? row.name : `${row.name}_${sub}`;
        const rankedList = rankStudentsByTest(global.profiles, global.tests, testKey);
        const studentRankObj = rankedList.find(s => s.roll === rollKey);
        if (studentRankObj && studentRankObj.rank !== '-') {
          row[`${sub}_Rank`] = studentRankObj.rank;
        }
      });

      const wt = weakMap[normRowName];
      if (wt) {
        ['Physics', 'Chemistry', 'Mathematics', 'Biology'].forEach((sub) => {
          const outSub = sub === 'Mathematics' ? 'Math' : sub;
          const metrics = wt.subjectMetrics?.[sub];
          if (metrics && metrics.attempted > 0) {
            row[`${outSub}_Attempted`] = metrics.attempted;
            row[`${outSub}_Correct`] = metrics.correct;
            row[`${outSub}_Accuracy`] = Math.round((metrics.correct / metrics.attempted) * 100);
          }
        });
        if (wt.attempted > 0) {
          row['Total_Attempted'] = wt.attempted;
          row['Total_Correct'] = wt.correct;
          row['Total_Accuracy'] = Math.round((wt.correct / wt.attempted) * 100);
        }
      }
      return row;
    });

    res.json({ chartData: finalChartData, weakSubject: weakSubj });
  } catch (e) {
    console.error('Error fetching student chart details', e);
    // fallback with error info for debugging
    chartData.push({ name: 'ERROR: ' + e.message, Physics: 0, Chemistry: 0, Math: 0, Biology: 0, Total: 0 });
    res.json({ chartData, weakSubject: weakSubj });
  }
});

/**
 * GET /api/analytics/centre-chart?centerCode=
 * Aggregates all students in a centre to provide chart-ready performance averages.
 */
app.get('/api/analytics/centre-chart', authenticateToken, async (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');

  const { centerCode } = req.query;
  if (!centerCode) return res.status(400).json({ message: 'centerCode is required' });

  try {
    const global = await loadApplicationData();
    const source = sliceCenterFromGlobal(global, centerCode);
    const centerTests = source.tests;
    const rollKeys = centerTests.map(t => t.ROLL_KEY);

    const chartData = buildCentreChartData(centerTests, source.testColumns);

    const weakTopics = await StudentWeakTopics.find({ studentId: { $in: rollKeys } }).lean();
    const weakMap = {};
    
    for (const wt of weakTopics) {
      const normKey = (wt.testId || '').replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
      if (!weakMap[normKey]) {
        weakMap[normKey] = {
          studentCountTotal: 0, totalAttempted: 0, totalCorrect: 0,
          subjectMetrics: {
            Physics: { attempted: 0, correct: 0, students: 0 },
            Chemistry: { attempted: 0, correct: 0, students: 0 },
            Mathematics: { attempted: 0, correct: 0, students: 0 },
            Biology: { attempted: 0, correct: 0, students: 0 },
          }
        };
      }
      
      const target = weakMap[normKey];
      if (wt.attempted > 0) {
         target.studentCountTotal++;
         target.totalAttempted += wt.attempted;
         target.totalCorrect += wt.correct;
      }
      
      if (wt.subjectMetrics) {
        ['Physics', 'Chemistry', 'Mathematics', 'Biology'].forEach(sub => {
          if (wt.subjectMetrics[sub] && wt.subjectMetrics[sub].attempted > 0) {
            target.subjectMetrics[sub].students++;
            target.subjectMetrics[sub].attempted += wt.subjectMetrics[sub].attempted;
            target.subjectMetrics[sub].correct += wt.subjectMetrics[sub].correct;
          }
        });
      }
    }

    for (const normKey of Object.keys(weakMap)) {
      if (!chartData.some(r => (r.name || '').replace(/[^a-zA-Z0-9]/g, '').toUpperCase() === normKey)) {
        const wtDoc = weakTopics.find(wt => (wt.testId || '').replace(/[^a-zA-Z0-9]/g, '').toUpperCase() === normKey);
        chartData.push({
          name: wtDoc ? wtDoc.testId : normKey,
          Physics: null, Chemistry: null, Math: null, Biology: null, Total: null
        });
      }
    }

    chartData.sort((a, b) => (a.name || '').localeCompare(b.name || '', undefined, { numeric: true }));

    const finalChartData = chartData.map((row) => {
      const normRowName = (row.name || '').replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
      const wt = weakMap[normRowName];
      if (wt) {
        ['Physics', 'Chemistry', 'Mathematics', 'Biology'].forEach((sub) => {
          const outSub = sub === 'Mathematics' ? 'Math' : sub;
          const metrics = wt.subjectMetrics?.[sub];
          if (metrics && metrics.students > 0) {
            row[`${outSub}_Attempted`] = Math.round(metrics.attempted / metrics.students);
            row[`${outSub}_Correct`] = Math.round(metrics.correct / metrics.students);
            row[`${outSub}_Accuracy`] = Math.round((metrics.correct / metrics.attempted) * 100);
          }
        });
        if (wt.studentCountTotal > 0) {
          row['Total_Attempted'] = Math.round(wt.totalAttempted / wt.studentCountTotal);
          row['Total_Correct'] = Math.round(wt.totalCorrect / wt.studentCountTotal);
          row['Total_Accuracy'] = Math.round((wt.totalCorrect / wt.totalAttempted) * 100);
        }
      }

      const testName = row.name;
      
      // Use computeTestInsights to guarantee 100% identical qualification rate as Leaderboard
      const insights = computeTestInsights(global.profiles, global.tests, testName, global.testColumns, {});
      
      const centreRow = insights.centreRows.find(r => r.code === centerCode);
      row.qualRate = centreRow && centreRow.appeared > 0 ? centreRow.qualRate : null;
      
      if (centreRow) {
        // Total Rank: centreRows is already sorted by totalAvg descending
        row['Total_Rank'] = insights.centreRows.findIndex(r => r.code === centerCode) + 1;
        
        // Subject Ranks
        ['Physics', 'Chemistry', 'Math', 'Biology'].forEach(sub => {
          
          // Filter centres that have a score for this subject
          const validCentres = insights.centreRows.filter(r => r.subjectAvgs[sub] !== null && r.subjectAvgs[sub] !== undefined);
          
          if (validCentres.some(r => r.code === centerCode)) {
            // Sort descending by subject average
            validCentres.sort((a, b) => b.subjectAvgs[sub] - a.subjectAvgs[sub]);
            const rank = validCentres.findIndex(r => r.code === centerCode) + 1;
            row[`${sub}_Rank`] = rank;
          }
        });
      }

      return row;
    });

    res.json({ chartData: finalChartData });
  } catch (e) {
    console.error('Error fetching centre chart details', e);
    res.status(500).json({ chartData: [], message: e.message });
  }
});

// TEMPORARY DEBUG ROUTE
app.get('/api/debug-chart/:rollKey', async (req, res) => {
  try {
    const rollKey = req.params.rollKey;
    const global = await loadApplicationData();
    const testDoc = global.tests.find((t) => t.ROLL_KEY === rollKey) || {};
    const chartData = buildStudentChartData(testDoc, global.testColumns);
    
    const weakTopics = await StudentWeakTopics.find({ studentId: rollKey }).lean();
    const weakMap = {};
    for (const wt of weakTopics) {
      const normKey = (wt.testId || '').replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
      weakMap[normKey] = wt;
    }

    const enrichedChartData = [...chartData];
    const finalChartData = enrichedChartData.map((row) => {
      const normRowName = (row.name || '').replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
      
      // Calculate global rankings for this test
      ['Total', 'Physics', 'Chemistry', 'Mathematics', 'Biology'].forEach((sub) => {
        const outSub = sub === 'Mathematics' ? 'Math' : sub;
        const testKey = `${row.name}-${sub}`;
        const rankedList = rankStudentsByTest(global.profiles, global.tests, testKey);
        const studentRankObj = rankedList.find(s => s.roll === rollKey);
        if (studentRankObj && studentRankObj.rank !== '-') {
          row[`${outSub}_Rank`] = studentRankObj.rank;
        }
      });

      const wt = weakMap[normRowName];
      if (wt) {
        ['Physics', 'Chemistry', 'Mathematics', 'Biology'].forEach((sub) => {
          const outSub = sub === 'Mathematics' ? 'Math' : sub;
          const metrics = wt.subjectMetrics?.[sub];
          if (metrics && metrics.attempted > 0) {
            row[`${outSub}_Attempted`] = metrics.attempted;
            row[`${outSub}_Correct`] = metrics.correct;
            row[`${outSub}_Accuracy`] = Math.round((metrics.correct / metrics.attempted) * 100);
          }
        });
        if (wt.attempted > 0) {
          row['Total_Attempted'] = wt.attempted;
          row['Total_Correct'] = wt.correct;
          row['Total_Accuracy'] = Math.round((wt.correct / wt.attempted) * 100);
        }
      }
      return row;
    });

    const StudentOverallWeakTopics = (await import('./models/StudentOverallWeakTopics.js')).default;
    const overallWeak = await StudentOverallWeakTopics.findOne({ studentId: rollKey }).lean();

    
    const rawFMT02 = await StudentRawMarks.findOne({ testId: 'FMT02', studentId: rollKey }).lean();
    const topicMapFMT02 = await TopicMap.findOne({ testId: 'FMT02' }).lean();
    const weakFMT02 = await StudentWeakTopics.findOne({ testId: 'FMT02', studentId: rollKey }).lean();
    
    // Simulate the fallback logic
    let marksEntries = [];
    if (rawFMT02 && rawFMT02.marks) {
      if (rawFMT02.marks instanceof Map) marksEntries = Array.from(rawFMT02.marks.entries());
      else if (typeof rawFMT02.marks === 'object' && rawFMT02.marks !== null) marksEntries = Object.entries(rawFMT02.marks);
    }
    
    let qToSub = {};
    if (topicMapFMT02) {
      (topicMapFMT02.topics || []).forEach(t => {
        (t.questions || []).forEach(q => {
          qToSub[q] = t.subject;
        });
      });
    }

    res.json({ 
      hasRaw: !!rawFMT02,
      rawMarksKeys: rawFMT02 ? Object.keys(rawFMT02.marks || {}).slice(0, 5) : [],
      marksEntriesCount: marksEntries.length,
      hasTopicMap: !!topicMapFMT02,
      topicMapTopicsCount: topicMapFMT02 ? (topicMapFMT02.topics || []).length : 0,
      qToSubKeysCount: Object.keys(qToSub).length,
      weakTopics: weakFMT02
    });

  } catch (e) {
    res.json({ error: e.message });
  }
});

/**
 * GET /api/analytics/test-columns
 * Return all known test columns and their parsed metadata.
 * Scoped to a centre if centerCode provided.
 */
app.get('/api/debug-state/:rollKey', async (req, res) => {
  try {
    const rollKey = req.params.rollKey;
    const rawMarks = await StudentRawMarks.find({ studentId: rollKey }).lean();
    const weakTopics = await StudentWeakTopics.find({ studentId: rollKey }).lean();
    const allRaw = await StudentRawMarks.find({ testId: 'FMT02' }).select('studentId').lean();
    
    
    const rawFMT02 = await StudentRawMarks.findOne({ testId: 'FMT02', studentId: rollKey }).lean();
    const topicMapFMT02 = await TopicMap.findOne({ testId: 'FMT02' }).lean();
    const weakFMT02 = await StudentWeakTopics.findOne({ testId: 'FMT02', studentId: rollKey }).lean();
    
    // Simulate the fallback logic
    let marksEntries = [];
    if (rawFMT02 && rawFMT02.marks) {
      if (rawFMT02.marks instanceof Map) marksEntries = Array.from(rawFMT02.marks.entries());
      else if (typeof rawFMT02.marks === 'object' && rawFMT02.marks !== null) marksEntries = Object.entries(rawFMT02.marks);
    }
    
    let qToSub = {};
    if (topicMapFMT02) {
      (topicMapFMT02.topics || []).forEach(t => {
        (t.questions || []).forEach(q => {
          qToSub[q] = t.subject;
        });
      });
    }

    res.json({ 
      hasRaw: !!rawFMT02,
      rawMarksKeys: rawFMT02 ? Object.keys(rawFMT02.marks || {}).slice(0, 5) : [],
      marksEntriesCount: marksEntries.length,
      hasTopicMap: !!topicMapFMT02,
      topicMapTopicsCount: topicMapFMT02 ? (topicMapFMT02.topics || []).length : 0,
      qToSubKeysCount: Object.keys(qToSub).length,
      weakTopics: weakFMT02
    });

  } catch(e) {
    res.status(500).json({ error: e.message });
  }
});

app.get('/api/analytics/test-columns', authenticateToken, async (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  const { centerCode } = req.query;
  const source = centerCode ? await loadCenterApplicationData(centerCode) : await loadApplicationData();
  const columns = source.testColumns;

  // Derive unique test names (total columns = no underscore / recognised total)
  const testNames = [...new Set(
    columns
      .filter((c) => !c.includes('_') && !c.match(/^(PHY|CHE|MAT|BIO|BOT|ZOO)\s/i))
      .map((c) => c)
  )];

  res.json({ columns, testNames });
});

// ── Student CRUD (Admin only) ──────────────────────────────────────────────────

/**
 * POST /api/students/bulk-upsert
 * High-performance bulk import: accepts an array of student objects and uses
 * MongoDB bulkWrite to insert/update ALL of them in a single database round-trip.
 * Body: { students: [ { ROLL_KEY, centerCode, ... }, ... ] }
 */
app.post('/api/students/bulk-upsert', authenticateToken, requireAdmin, async (req, res) => {
  const { students } = req.body;
  if (!Array.isArray(students) || students.length === 0) {
    return res.status(400).json({ message: 'students array is required' });
  }

  try {
    if (!isDbEnabled()) {
      return res.status(500).json({ message: 'Database not enabled' });
    }

    await initMongo();

    const ops = students.map((student) => {
      const roll = normalizeRollKey(student.ROLL_KEY);
      const center = normalizeCenterCode(student.centerCode);
      if (!roll || !center) return null;

      // MongoDB does not allow dots in field names.
      const sanitizedStudent = {};
      for (const [k, v] of Object.entries(student)) {
        const safeKey = k.replace(/\./g, '___dot___');
        sanitizedStudent[safeKey] = v;
      }

      const doc = { ...sanitizedStudent, ROLL_KEY: roll, centerCode: center };
      if (!doc.stream) doc.stream = 'JEE';

      return {
        updateOne: {
          filter: { ROLL_KEY: roll, centerCode: center },
          update: { $set: doc },
          upsert: true,
        },
      };
    }).filter(Boolean);

    if (ops.length === 0) {
      return res.status(400).json({ message: 'No valid students in array' });
    }

    const Profile = (await import('./models/Profile.js')).default;
    const result = await Profile.bulkWrite(ops, { ordered: false });

    invalidateDataCache();

    const inserted = result.upsertedCount || 0;
    const modified = result.modifiedCount || 0;
    console.log(`[BULK] Bulk upsert: ${inserted} inserted, ${modified} updated out of ${ops.length} students`);

    
    const rawFMT02 = await StudentRawMarks.findOne({ testId: 'FMT02', studentId: rollKey }).lean();
    const topicMapFMT02 = await TopicMap.findOne({ testId: 'FMT02' }).lean();
    const weakFMT02 = await StudentWeakTopics.findOne({ testId: 'FMT02', studentId: rollKey }).lean();
    
    // Simulate the fallback logic
    let marksEntries = [];
    if (rawFMT02 && rawFMT02.marks) {
      if (rawFMT02.marks instanceof Map) marksEntries = Array.from(rawFMT02.marks.entries());
      else if (typeof rawFMT02.marks === 'object' && rawFMT02.marks !== null) marksEntries = Object.entries(rawFMT02.marks);
    }
    
    let qToSub = {};
    if (topicMapFMT02) {
      (topicMapFMT02.topics || []).forEach(t => {
        (t.questions || []).forEach(q => {
          qToSub[q] = t.subject;
        });
      });
    }

    return res.json({ 
      hasRaw: !!rawFMT02,
      rawMarksKeys: rawFMT02 ? Object.keys(rawFMT02.marks || {}).slice(0, 5) : [],
      marksEntriesCount: marksEntries.length,
      hasTopicMap: !!topicMapFMT02,
      topicMapTopicsCount: topicMapFMT02 ? (topicMapFMT02.topics || []).length : 0,
      qToSubKeysCount: Object.keys(qToSub).length,
      weakTopics: weakFMT02
    });

  } catch (e) {
    console.error('[BULK] Bulk upsert failed:', e);
    return res.status(500).json({ message: e.message || 'Bulk upsert failed' });
  }
});

app.post('/api/students', authenticateToken, requireAdmin, async (req, res) => {
  const student = req.body;
  if (!student.ROLL_KEY) return res.status(400).json({ message: 'ROLL_KEY is required' });
  if (!student.centerCode) return res.status(400).json({ message: 'centerCode is required' });

  // Default stream to JEE
  if (!student.stream) student.stream = 'JEE';

  const globalData = await loadApplicationData();
  const exists = globalData.profiles.find(
    (p) => p.centerCode === student.centerCode && p.ROLL_KEY === student.ROLL_KEY
  );
  if (exists) {
    return res.status(409).json({ message: 'Student with this roll already exists at this centre' });
  }

  try {
    if (isDbEnabled()) {
      await upsertProfileDoc(student);
    } else {
      globalData.profiles.push(student);
    }
    const fresh = await loadApplicationData();
    const saved = fresh.profiles.find(
      (p) => p.centerCode === student.centerCode && p.ROLL_KEY === student.ROLL_KEY
    );
    console.log(`[CRUD] Added student: ${student.ROLL_KEY}`);
    return res.status(201).json({ success: true, student: saved });
  } catch (e) {
    console.error('[CRUD] Add student failed:', e);
    return res.status(500).json({ message: e.message || 'Save failed' });
  }
});

app.put('/api/students/:rollKey', authenticateToken, requireAdmin, async (req, res) => {
  const { rollKey } = req.params;
  const centerCode = req.query.centerCode;
  const globalData = await loadApplicationData();
  const idx = findProfileIndex(globalData, rollKey, centerCode);

  if (idx === -2) return res.status(400).json({ message: 'Multiple students share this roll; pass centerCode query' });
  if (idx === -1) return res.status(404).json({ message: 'Student not found' });

  const merged = { ...globalData.profiles[idx], ...req.body, ROLL_KEY: rollKey };

  try {
    if (isDbEnabled()) {
      await upsertProfileDoc(merged);
    } else {
      globalData.profiles[idx] = merged;
    }
    const fresh = await loadApplicationData();
    const updated = fresh.profiles.find(
      (p) => p.ROLL_KEY === rollKey && p.centerCode === merged.centerCode
    );
    console.log(`[CRUD] Updated student: ${rollKey}`);
    return res.json({ success: true, student: updated });
  } catch (e) {
    console.error('[CRUD] Update student failed:', e);
    return res.status(500).json({ message: e.message || 'Update failed' });
  }
});

/**
 * POST /api/students/bulk-delete
 * Fast deletion of multiple students using MongoDB $in operator.
 * Body: { rollKeys: ["roll1", "roll2", ...] }
 */
app.post('/api/students/bulk-delete', authenticateToken, requireAdmin, async (req, res) => {
  const { rollKeys } = req.body;
  if (!Array.isArray(rollKeys) || rollKeys.length === 0) {
    return res.status(400).json({ message: 'rollKeys array is required' });
  }

  try {
    if (!isDbEnabled()) {
      return res.status(500).json({ message: 'Database not enabled' });
    }
    await initMongo();
    const Profile = (await import('./models/Profile.js')).default;
    const TestScore = (await import('./models/TestScore.js')).default;

    const profileResult = await Profile.deleteMany({ ROLL_KEY: { $in: rollKeys } });
    await TestScore.deleteMany({ ROLL_KEY: { $in: rollKeys } });

    invalidateDataCache();
    console.log(`[BULK] Deleted ${profileResult.deletedCount} student profiles for ${rollKeys.length} requested keys.`);

    return res.json({ success: true, deletedCount: profileResult.deletedCount });
  } catch (e) {
    console.error('[BULK] Bulk delete failed:', e);
    return res.status(500).json({ message: e.message || 'Bulk delete failed' });
  }
});

app.delete('/api/students/:rollKey', authenticateToken, requireAdmin, async (req, res) => {
  const { rollKey } = req.params;
  const centerCode = req.query.centerCode;
  const globalData = await loadApplicationData();
  const idx = findProfileIndex(globalData, rollKey, centerCode);

  if (idx === -2) return res.status(400).json({ message: 'Multiple students share this roll; pass centerCode query' });
  if (idx === -1) return res.status(404).json({ message: 'Student not found' });

  const cc = globalData.profiles[idx].centerCode;

  try {
    if (isDbEnabled()) {
      await deleteStudentDocs(cc, rollKey);
    } else {
      globalData.profiles.splice(idx, 1);
      const tIdx = globalData.tests.findIndex(
        (t) => t.ROLL_KEY === rollKey && t.centerCode === cc
      );
      if (tIdx !== -1) globalData.tests.splice(tIdx, 1);
    }
    console.log(`[CRUD] Deleted student: ${rollKey}`);
    return res.json({ success: true });
  } catch (e) {
    console.error('[CRUD] Delete student failed:', e);
    return res.status(500).json({ message: e.message || 'Delete failed' });
  }
});

// ── Test Score Upsert (Admin only) ────────────────────────────────────────────

/**
 * POST /api/tests/bulk-upsert
 * High-performance bulk import for test scores.
 * Body: { marks: [ { rollKey, centerCode, scores }, ... ] }
 */
app.post('/api/tests/bulk-upsert', authenticateToken, requireAdmin, async (req, res) => {
  const { marks } = req.body;
  if (!Array.isArray(marks) || marks.length === 0) {
    return res.status(400).json({ message: 'marks array is required' });
  }

  try {
    if (!isDbEnabled()) {
      return res.status(500).json({ message: 'Database not enabled' });
    }
    await initMongo();
    const TestScore = (await import('./models/TestScore.js')).default;

    const ops = marks.map((mark) => {
      const roll = normalizeRollKey(mark.rollKey);
      const center = normalizeCenterCode(mark.centerCode);
      if (!roll || !center) return null;

      const $setObj = { stream: mark.scores?.stream || 'JEE' };
      
      let patchNested;
      if (mark.scores && typeof mark.scores.tests === 'object') {
        patchNested = { tests: mark.scores.tests };
      } else {
        patchNested = flatToNested(mark.scores || {});
      }

      if (patchNested.tests) {
        for (const [testName, testData] of Object.entries(patchNested.tests)) {
          for (const [subject, value] of Object.entries(testData)) {
            // MongoDB safe key (dots are not allowed in object keys, but here we intentionally use them for update paths)
            const safeTestName = testName.replace(/\./g, '___dot___');
            const safeSubject = subject.replace(/\./g, '___dot___');
            $setObj[`tests.${safeTestName}.${safeSubject}`] = value;
          }
        }
      }

      return {
        updateOne: {
          filter: { ROLL_KEY: roll, centerCode: center },
          update: { $set: $setObj },
          upsert: true,
        },
      };
    }).filter(Boolean);

    if (ops.length === 0) {
      return res.status(400).json({ message: 'No valid marks in array' });
    }

    const result = await TestScore.bulkWrite(ops, { ordered: false });
    invalidateDataCache();
    console.log(`[BULK] Upserted ${marks.length} test scores`);

    return res.json({ 
      success: true, 
      matchedCount: result.matchedCount,
      modifiedCount: result.modifiedCount,
      upsertedCount: result.upsertedCount
    });
  } catch (e) {
    console.error('[BULK] Bulk upsert tests failed:', e);
    return res.status(500).json({ message: e.message || 'Bulk upsert tests failed' });
  }
});

/**
 * POST /api/tests/:rollKey?centerCode=
 * Body can be:
 *   { scores: { "CAT-1(TEST)_Physics": 45, "CAT-1(TEST)": 145, ... } }  (flat)
 *   { scores: { tests: { "CAT-1(TEST)": { Physics: 45, total: 145 } } } } (nested patch)
 */
app.post('/api/tests/:rollKey', authenticateToken, requireAdmin, async (req, res) => {
  const { rollKey } = req.params;
  const centerCode = req.query.centerCode;
  const { scores } = req.body;

  const globalData = await loadApplicationData();
  const profile = findProfile(globalData, rollKey, centerCode);

  if (!profile) {
    if (!centerCode && globalData.profiles.filter((p) => normalizeRollKey(p.ROLL_KEY) === normalizeRollKey(rollKey)).length > 1) {
      return res.status(400).json({ message: 'Multiple students share this roll; pass centerCode query' });
    }
    return res.status(404).json({ message: 'Student not found' });
  }

  const cc = profile.centerCode;

  try {
    if (isDbEnabled()) {
      const testRecord = await upsertTestDoc(cc, rollKey, scores);
      console.log(`[CRUD] Upserted test scores for: ${rollKey}`);
      return res.json({ success: true, testRecord });
    }

    // In-memory fallback
    let testRecord = globalData.tests.find(
      (t) => t.ROLL_KEY === rollKey && t.centerCode === cc
    );
    if (!testRecord) {
      testRecord = { ROLL_KEY: rollKey, centerCode: cc };
      globalData.tests.push(testRecord);
    }
    Object.assign(testRecord, scores);
    console.log(`[CRUD] Upserted test scores for: ${rollKey}`);
    return res.json({ success: true, testRecord });
  } catch (e) {
    console.error('[CRUD] Test upsert failed:', e);
    return res.status(500).json({ message: e.message || 'Save failed' });
  }
});

/**
 * DELETE /api/admin/tests/:testKey
 * Format (delete) all marks and analytics data for a specific test.
 */
app.delete('/api/admin/tests/:testKey', authenticateToken, requireAdmin, async (req, res) => {
  const { testKey } = req.params;
  try {
    if (isDbEnabled()) {
      await initMongo();
      
      const updateResult = await TestScore.updateMany(
        {},
        { $unset: { [`tests.${testKey}`]: "" } }
      );
      
      const res1 = await StudentWeakTopics.deleteMany({ testId: testKey });
      const res2 = await CenterWeakTopics.deleteMany({ testId: testKey });
      const res3 = await TopicMap.deleteMany({ testId: testKey });
      const res4 = await StudentRawMarks.deleteMany({ testId: testKey });
      
      invalidateDataCache();
      console.log(`[CRUD] Formatted test data for ${testKey} | Scores updated: ${updateResult.modifiedCount} | SRM: ${res4.deletedCount}`);
      return res.json({ success: true, message: `Successfully formatted test data for ${testKey}` });
    } else {
       const globalData = await loadApplicationData();
       globalData.tests.forEach(t => {
         if (t[testKey] !== undefined) delete t[testKey];
       });
       return res.json({ success: true, message: `Formatted test data (memory) for ${testKey}` });
    }
  } catch (e) {
    console.error('[CRUD] Format test failed:', e);
    return res.status(500).json({ message: e.message || 'Format failed' });
  }
});

// ── Weak Topics — Admin Routes ────────────────────────────────────────────────

const upload = multer({ storage: multer.memoryStorage() });

/**
 * DELETE /api/admin/weak-topics/clear
 * Clear all weak topics data across all collections.
 */
app.delete('/api/admin/weak-topics/clear', authenticateToken, requireAdmin, async (req, res) => {
  try {
    await initMongo();
    await CenterWeakTopics.deleteMany({});
    await StudentWeakTopics.deleteMany({});
    await CenterOverallWeakTopics.deleteMany({});
    await StudentOverallWeakTopics.deleteMany({});
    console.log('[WeakTopics] All weak topic data cleared.');
    return res.json({ success: true, message: 'All weak topic data has been cleared.' });
  } catch (e) {
    console.error('[WeakTopics] Clear error:', e);
    return res.status(500).json({ success: false, message: e.message || 'Failed to clear weak topics data.' });
  }
});

/**
 * DELETE /api/admin/raw-marks/clear
 * Clear all marks-awarded-sheet (StudentRawMarks) data. Admin only.
 */
app.delete('/api/admin/raw-marks/clear', authenticateToken, requireAdmin, async (req, res) => {
  try {
    const { testId } = req.query;
    await initMongo();
    if (testId) {
      const result = await StudentRawMarks.deleteMany({ testId });
      console.log(`[RawMarks] Cleared ${result.deletedCount} records for testId="${testId}".`);
      return res.json({ success: true, message: `Cleared ${result.deletedCount} records for test "${testId}".`, deletedCount: result.deletedCount });
    }
    const result = await StudentRawMarks.deleteMany({});
    console.log(`[RawMarks] All raw marks cleared (${result.deletedCount} records).`);
    return res.json({ success: true, message: `All marks awarded data cleared (${result.deletedCount} records).`, deletedCount: result.deletedCount });
  } catch (e) {
    console.error('[RawMarks] Clear error:', e);
    return res.status(500).json({ success: false, message: e.message || 'Failed to clear marks data.' });
  }
});

/**
 * POST /api/admin/weak-topics/upload-test-sheet
 * Upload a unified test sheet (CSV) containing headers, topic row, answer-key row,
 * and all student marks in a single file — no paper1/paper2 split.
 *
 * Sheet format:
 *   Row 1: LOCATION | ROLL NO. | NAME | Q1 | Q2 | … | Qn  (headers)
 *   Row 2: (blank)  | (blank)  | (blank) | Kinematics | Laws of Motion | …  (topic per question)
 *   Row 3: (blank)  | (blank)  | (blank) | A | B | …  (answer key — stored only)
 *   Row 4+: student data rows
 *
 * Body fields: testId (string)
 * File field:  file (.csv)
 *
 * Returns a diagnostic summary:
 *   { success, testId, studentsProcessed, studentsAbsent, topicsFound,
 *     smallQuestionTopics, centersProcessed, warnings }
 */
app.post('/api/admin/weak-topics/upload-test-sheet', authenticateToken, requireAdmin, upload.single('file'), async (req, res) => {
  try {
    const { testId } = req.body;
    if (!testId)   return res.status(400).json({ success: false, message: 'testId is required' });
    if (!req.file) return res.status(400).json({ success: false, message: 'CSV file is required' });

    await initMongo();

    // Seed topic→subject lookup from DB syllabus (best-effort; sheet prefix format also works)
    try {
      const syllabusEntries = await SyllabusTopics.find({}).lean();
      if (syllabusEntries.length > 0) buildTopicSubjectLookup(syllabusEntries);
    } catch (e) {
      console.warn('[WeakTopics] Could not load SyllabusTopics for subject inference:', e.message);
    }

    // Parse the sheet — throws with .validationErrors if sheet is malformed
    let parsed;
    try {
      parsed = parseTestSheet(req.file.buffer);
    } catch (parseErr) {
      const errors = parseErr.validationErrors || [parseErr.message];
      return res.status(422).json({
        success:          false,
        message:          'Test sheet validation failed. Fix the errors below and re-upload.',
        validationErrors: errors,
      });
    }

    const {
      topicsWithQuestions,
      smallQuestionTopics,
      unknownSubjectQuestions,
      students,
      questionTopicMap,
    } = parsed;

    // Idempotent: delete existing raw marks for this testId, then re-insert
    await StudentRawMarks.deleteMany({ testId });

    // Upsert TopicMap (single doc per testId)
    const topicEntries = Object.entries(topicsWithQuestions).map(([topic, { questions, subject }]) => ({
      topic,
      subject,
      questions,
      questionCount: questions.length,
    }));
    await TopicMap.findOneAndUpdate(
      { testId },
      { $set: { topics: topicEntries } },
      { upsert: true, new: true, setDefaultsOnInsert: true }
    );

    // Insert student raw marks
    if (students.length > 0) {
      const marksDocs = students.map((s) => ({
        studentId:   s.studentId,
        testId,
        centerId:    s.centerId,
        studentName: s.name,
        marks:       s.marks,
      }));
      await StudentRawMarks.insertMany(marksDocs, { ordered: false });
    }

    // Compute weak topics immediately (no paper-count gate needed anymore)
    let computeResult = { studentsProcessed: 0, studentsAbsent: 0, topicsFound: 0, smallQuestionTopics: [], centersProcessed: 0 };
    try {
      computeResult = await computeWeakTopics(testId);
    } catch (e) {
      console.error('[WeakTopics] computeWeakTopics error after upload:', e);
      // Don't fail the request — data is saved; computation can be retried
    }

    const warnings = [];
    if (smallQuestionTopics.length > 0) {
      warnings.push(
        `Topics with fewer than 3 questions (quantization warning — "Weak" band may not trigger): ` +
        smallQuestionTopics.join(', ')
      );
    }

    return res.json({
      success:             true,
      testId,
      studentsIngested:    students.length,
      studentsProcessed:   computeResult.studentsProcessed,
      studentsAbsent:      computeResult.studentsAbsent,
      topicsFound:         computeResult.topicsFound,
      smallQuestionTopics: computeResult.smallQuestionTopics,
      centersProcessed:    computeResult.centersProcessed,
      message:             `Test sheet for ${testId} processed successfully.`,
      warnings,
    });
  } catch (e) {
    console.error('[WeakTopics] upload-test-sheet error:', e);
    return res.status(500).json({ success: false, message: e.message || 'Failed to process test sheet' });
  }
});

// ── Weak Topics — Student Routes ───────────────────────────────────────────────

/**
 * GET /api/student/weak-topics/:studentId?testId=
 * Get weak topic analysis for a student.
 */
app.get('/api/student/weak-topics/:studentId', authenticateToken, async (req, res) => {
  try {
    const { studentId } = req.params;
    const { testId } = req.query;

    await initMongo();

    if (testId) {
      const doc = await StudentWeakTopics.findOne({ studentId, testId }).lean();
      return res.json({ success: true, data: doc || {} });
    }

    const docs = await StudentWeakTopics.find({ studentId }).sort({ testId: 1 }).lean();
    const filtered = docs.filter(d => d.testId && d.testId.length > 1 && d.testId !== 'CAT4');
    return res.json({ success: true, data: filtered });
  } catch (e) {
    console.error('[WeakTopics] student route error:', e);
    return res.status(500).json({ success: false, message: e.message || 'Failed to fetch student weak topics' });
  }
});

// ── Weak Topics — Center Routes ────────────────────────────────────────────────

/**
 * GET /api/center/weak-topics/:centerId?testId=
 * Get weak topic analysis for a center.
 */
app.get('/api/center/weak-topics/:centerId', authenticateToken, async (req, res) => {
  try {
    let { centerId } = req.params;
    const { testId } = req.query;
    // Normalize physical centre codes from frontend to sponsor/alias codes stored in the DB
    if (centerId === 'KNP') centerId = 'GAIL';
    if (centerId === 'JDH') centerId = 'OIL_INDIA';

    await initMongo();

    if (testId) {
      const doc = await CenterWeakTopics.findOne({ centerId, testId }).lean();
      return res.json({ success: true, data: doc || {} });
    }

    const docs = await CenterWeakTopics.find({ centerId }).sort({ testId: 1 }).lean();
    const filtered = docs.filter(d => d.testId && d.testId.length > 1 && d.testId !== 'CAT4');
    return res.json({ success: true, data: filtered });
  } catch (e) {
    console.error('[WeakTopics] center route error:', e);
    return res.status(500).json({ success: false, message: e.message || 'Failed to fetch center weak topics' });
  }
});

/**
 * GET /api/student/overall-weak-topics/:studentId
 * Get overall weak topic analysis for a student across all tests.
 */
app.get('/api/student/overall-weak-topics/:studentId', authenticateToken, async (req, res) => {
  try {
    const { studentId } = req.params;
    await initMongo();
    const doc = await StudentOverallWeakTopics.findOne({ studentId }).lean();
    return res.json({ success: true, data: doc || {} });
  } catch (e) {
    console.error('[WeakTopics] student overall route error:', e);
    return res.status(500).json({ success: false, message: e.message || 'Failed to fetch student overall weak topics' });
  }
});

/**
 * GET /api/center/overall-weak-topics/:centerId
 * Get overall weak topic analysis for a center across all tests.
 */
app.get('/api/center/overall-weak-topics/:centerId', authenticateToken, async (req, res) => {
  try {
    let { centerId } = req.params;
    // Normalize physical centre codes from frontend to sponsor/alias codes stored in the DB
    if (centerId === 'KNP') centerId = 'GAIL';
    if (centerId === 'JDH') centerId = 'OIL_INDIA';
    await initMongo();
    const doc = await CenterOverallWeakTopics.findOne({ centerId }).lean();
    return res.json({ success: true, data: doc || {} });
  } catch (e) {
    console.error('[WeakTopics] center overall route error:', e);
    return res.status(500).json({ success: false, message: e.message || 'Failed to fetch center overall weak topics' });
  }
});

// ── Past Year Data Management (separate from main data) ───────────────────────

// Upload past year data (admin only) — expects JSON array from frontend Excel parse
app.post('/api/past-year-data/upload', authenticateToken, async (req, res) => {
  if (req.user.role !== 'admin') return res.status(403).json({ message: 'Admin only' });
  try {
    const rows = req.body.rows;
    if (!Array.isArray(rows) || rows.length === 0) {
      return res.status(400).json({ message: 'No rows provided' });
    }
    // Insert all rows into PastYearData collection
    const result = await PastYearData.insertMany(rows, { ordered: false });
    return res.json({ success: true, inserted: result.length });
  } catch (e) {
    console.error('[PastYearData] upload error:', e);
    return res.status(500).json({ message: e.message || 'Upload failed' });
  }
});

// Get past year data with optional filters
app.get('/api/past-year-data', authenticateToken, async (req, res) => {
  if (req.user.role !== 'admin' && req.user.role !== 'centre') {
    return res.status(403).json({ message: 'Forbidden' });
  }
  try {
    const filter = {};
    if (req.query.year) filter.Year = req.query.year;
    if (req.query.sponsor) filter.Sponsor = { $regex: new RegExp(req.query.sponsor, 'i') };
    if (req.query.centre) filter['Centre Code'] = { $regex: new RegExp(req.query.centre, 'i') };
    if (req.query.state) filter.STATE = { $regex: new RegExp(req.query.state, 'i') };
    if (req.query.category) filter.Category = { $regex: new RegExp(req.query.category, 'i') };
    if (req.query.gender) filter.Gender = { $regex: new RegExp(req.query.gender, 'i') };
    if (req.query.remark) filter['ADMISSION REMARKS'] = { $regex: new RegExp(req.query.remark, 'i') };

    const docs = await PastYearData.find(filter).lean();
    return res.json({ success: true, data: docs });
  } catch (e) {
    console.error('[PastYearData] fetch error:', e);
    return res.status(500).json({ message: e.message || 'Fetch failed' });
  }
});

// Get distinct filter values for dropdowns
app.get('/api/past-year-data/filters', authenticateToken, async (req, res) => {
  if (req.user.role !== 'admin' && req.user.role !== 'centre') {
    return res.status(403).json({ message: 'Forbidden' });
  }
  try {
    const [years, sponsors, centres, states, categories, genders, remarks] = await Promise.all([
      PastYearData.distinct('Year'),
      PastYearData.distinct('Sponsor'),
      PastYearData.distinct('Centre Code'),
      PastYearData.distinct('STATE'),
      PastYearData.distinct('Category'),
      PastYearData.distinct('Gender'),
      PastYearData.distinct('ADMISSION REMARKS'),
    ]);
    return res.json({
      success: true,
      years: years.filter(Boolean).sort(),
      sponsors: sponsors.filter(Boolean).sort(),
      centres: centres.filter(Boolean).sort(),
      states: states.filter(Boolean).sort(),
      categories: categories.filter(Boolean).sort(),
      genders: genders.filter(Boolean).sort(),
      remarks: remarks.filter(Boolean).sort(),
    });
  } catch (e) {
    console.error('[PastYearData] filters error:', e);
    return res.status(500).json({ message: e.message || 'Fetch filters failed' });
  }
});

// Delete all past year data (admin only)
app.delete('/api/past-year-data', authenticateToken, async (req, res) => {
  if (req.user.role !== 'admin') return res.status(403).json({ message: 'Admin only' });
  try {
    const filter = {};
    if (req.query.year) filter.Year = req.query.year;
    if (req.query.sponsor) filter.Sponsor = req.query.sponsor;
    const result = await PastYearData.deleteMany(filter);
    return res.json({ success: true, deleted: result.deletedCount });
  } catch (e) {
    console.error('[PastYearData] delete error:', e);
    return res.status(500).json({ message: e.message || 'Delete failed' });
  }
});

// ── Errors (async route failures + thrown errors) ─────────────────────────────

app.use((err, req, res, next) => {
  void next;
  console.error('[API]', req.method, req.path, err);
  const status = Number(err.statusCode || err.status) || 500;
  const message =
    err.message ||
    (status === 500 ? 'Internal Server Error' : 'Request failed');
  res.status(status).json({
    message,
    ...(process.env.NODE_ENV !== 'production' && err.stack ? { detail: err.stack } : {}),
  });
});

// ── Server Start ──────────────────────────────────────────────────────────────

app.listen(PORT, async () => {
  console.log(`[Server] Core API Backend running on port ${PORT}`);

  try {
    if (process.env.MONGODB_URI || process.env.MONGO_URI) {
      await initMongo();
      await seedTopics(); // Seed the syllabus right after connecting!
    }
    const mongoStatus = isMongoReady();
    console.log("Mongo Ready Status:", mongoStatus);
  } catch (e) {
    console.log("Mongo Check Error:", e);
  }
});