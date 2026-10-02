import { correctedTopicSubject } from './normalizeTopicSubjects.js';

// Verified against the supplied NCT01 paper: four consecutive 45-question sections.
// Do not apply this layout to other tests without a verified paper definition.
export function verifiedQuestionSubject(testId, question) {
  if (String(testId || '').trim().toUpperCase() !== 'NCT01') return null;
  const n = Number(String(question).replace(/^Q/i, ''));
  if (!Number.isInteger(n) || n < 1 || n > 180) return null;
  return ['PHYSICS', 'CHEMISTRY', 'BOTANY', 'ZOOLOGY'][Math.floor((n - 1) / 45)];
}

export function normalizeTestTopicMap(doc) {
  if (!doc?.topics) return doc;
  const topics = [];
  for (const entry of doc.topics) {
    const groups = new Map();
    for (const q of entry.questions || []) {
      const subject = verifiedQuestionSubject(doc.testId, q)
        || correctedTopicSubject(entry.topic)
        || String(entry.subject || '').trim().toUpperCase();
      if (!groups.has(subject)) groups.set(subject, []);
      groups.get(subject).push(q);
    }
    for (const [subject, questions] of groups) topics.push({ ...entry, subject, questions, questionCount: questions.length });
  }
  return { ...doc, topics };
}

// Repair derived NCT01 scores on read, without changing uploaded marks in MongoDB.
export function applyVerifiedRawScores(data, rawDocs, parseTestColumn) {
  const byRoll = new Map(data.tests.map(row => [String(row.ROLL_KEY).trim(), row]));
  const cols = new Set(data.testColumns);
  const display = { PHYSICS: 'Physics', CHEMISTRY: 'Chemistry', BOTANY: 'Botany', ZOOLOGY: 'Zoology' };
  for (const doc of rawDocs) {
    if (String(doc.testId).trim().toUpperCase() !== 'NCT01') continue;
    const row = byRoll.get(String(doc.studentId).trim());
    if (!row) continue;
    const marks = doc.marks instanceof Map ? Object.fromEntries(doc.marks) : doc.marks || {};
    const scores = { Physics: 0, Chemistry: 0, Botany: 0, Zoology: 0, Total: 0 };
    let count = 0;
    for (let n = 1; n <= 180; n++) {
      const raw = marks[`Q${n}`];
      if (raw === null || raw === undefined || String(raw).trim() === '' || !Number.isFinite(Number(raw))) continue;
      const v = Number(raw);
      scores[display[verifiedQuestionSubject('NCT01', `Q${n}`)]] += v;
      scores.Total += v;
      count++;
    }
    // Never turn an absent or incomplete raw sheet into fabricated zero scores.
    if (count !== 180) continue;
    for (const key of Object.keys(row)) {
      const { testName, subject, isTotal } = parseTestColumn(key);
      if (testName === 'NCT01' && (isTotal || subject in scores)) row[key] = scores[isTotal ? 'Total' : subject];
    }
    for (const [subject, value] of Object.entries(scores)) {
      const key = subject === 'Total' ? 'NCT01' : `NCT01_${subject}`;
      row[key] = value;
      cols.add(key);
    }
  }
  data.testColumns = [...cols];
  return data;
}
