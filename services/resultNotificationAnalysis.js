import { parseTestColumn } from '../utils/testColumns.js';
// Snapshot calculations mirror the existing qualification summary without changing it.
export function buildQualificationSummary(data, centreBoard, testKey, stream) {
  const subjects = stream === 'NEET' ? ['Physics', 'Chemistry', 'Botany', 'Zoology'] : ['Physics', 'Chemistry', 'Math'];
  const keys = testKey === 'ALL_FMT' ? [...new Set((data?.testColumns || []).filter(k => k.startsWith('FMT')).map(k => k.split('_')[0]))] : String(testKey || '').split(',').map(k => k.trim()).filter(Boolean);
  const numeric = value => value !== null && value !== undefined && String(value).trim() !== '' && Number.isFinite(Number(value)) ? Number(value) : null;
  const mean = values => values.length ? values.reduce((a, b) => a + b, 0) / values.length : null;
  const profileMap = new Map((data?.profiles || []).map(p => [String(p.ROLL_KEY), p]));
  const buckets = new Map(centreBoard.map(c => [c.code, []]));
  const seen = new Set();
  for (const doc of data?.tests || []) {
    const profile = profileMap.get(String(doc.ROLL_KEY));
    if (!profile || !buckets.has(profile.centerCode) || seen.has(String(doc.ROLL_KEY))) continue;
    seen.add(String(doc.ROLL_KEY));
    const values = {};
    for (const subject of [...subjects, 'Total']) {
      for (const suffix of ['', '_Attempted', '_Accuracy']) {
        const samples = keys.map(key => {
          const column = Object.keys(doc).find(col => {
            const meta = parseTestColumn(col);
            const normalized = meta.subject.replace(/^Mathematics|^Maths/, 'Math');
            return meta.testName === key && normalized === subject + suffix;
          });
          return column ? numeric(doc[column]) : null;
        }).filter(v => v !== null);
        values[subject + suffix] = mean(samples);
      }
    }
    // Derive only totals supported by complete subject records.
    if (values.Total === null && subjects.every(sub => values[sub] !== null)) values.Total = subjects.reduce((sum, sub) => sum + values[sub], 0);
    if (values.Total === null) continue;
    if (values.Total_Attempted === null && subjects.every(sub => values[sub + '_Attempted'] !== null)) {
      values.Total_Attempted = subjects.reduce((sum, sub) => sum + values[sub + '_Attempted'], 0);
    }
    if (values.Total_Accuracy === null && values.Total_Attempted > 0 && subjects.every(sub => values[sub + '_Attempted'] !== null && values[sub + '_Accuracy'] !== null)) {
      values.Total_Accuracy = subjects.reduce((sum, sub) => sum + values[sub + '_Attempted'] * values[sub + '_Accuracy'], 0) / values.Total_Attempted;
    }
    buckets.get(profile.centerCode).push(values);
  }
  const aggregate = students => Object.fromEntries([...subjects, 'Total'].flatMap(sub => ['', '_Attempted', '_Accuracy'].map(suffix => {
    const key = sub + suffix;
    return [key, mean(students.map(s => s[key]).filter(v => v !== null))];
  })));
  const rows = [...centreBoard].sort((a, b) => b.avg - a.avg || a.code.localeCompare(b.code)).map((centre, index) => ({
    rank: index + 1, code: centre.code, appeared: centre.tested || 0, qualified: centre.qualifiedCount || 0,
    ...aggregate(buckets.get(centre.code)), Total: centre.avg,
  }));
  for (const subject of subjects) {
    const sorted = rows.filter(row => row[subject] !== null).sort((a, b) => b[subject] - a[subject] || a.code.localeCompare(b.code));
    sorted.forEach((row, index) => { row[subject + '_Rank'] = index + 1; });
  }
  const appeared = rows.reduce((sum, row) => sum + row.appeared, 0);
  const overall = { code: 'OVERALL', appeared, qualified: rows.reduce((sum, row) => sum + row.qualified, 0),
    ...aggregate([...buckets.values()].flat()),
    Total: appeared ? rows.reduce((sum, row) => sum + row.Total * row.appeared, 0) / appeared : null };
  return { subjects, rows, overall };
}

export function qualificationMetrics(scoped, testKey, stream, docs, maps) {
 const allowed = new Map(scoped.profiles.map(p => [String(p.ROLL_KEY).trim(), p.centerCode]));
    const aliases = { PHYSICS: 'Physics', PHY: 'Physics', CHEMISTRY: 'Chemistry', CHEM: 'Chemistry', MATHEMATICS: 'Math', MATH: 'Math', MATHS: 'Math', BOTANY: 'Botany', ZOOLOGY: 'Zoology', BIOLOGY: 'Biology' };
    const questions = new Map(maps.map(map => {
      const lookup = new Map();
      for (const topic of map.topics || []) {
        const subject = aliases[String(topic.subject).trim().toUpperCase()];
        if (!subject || (stream === 'NEET' ? subject === 'Math' : ['Botany', 'Zoology', 'Biology'].includes(subject))) continue;
        for (const q of topic.questions || []) lookup.set(String(q), subject);
      }
      return [map.testId, lookup];
    }));
    const byCentre = {};
    const overall = {};
    const add = (target, subject, metric) => {
      const item = target[subject] ||= { attempted: 0, correct: 0, records: 0 };
      item.attempted += metric.attempted; item.correct += metric.correct; item.records++;
    };
    const seen = new Set();
    for (const doc of docs) {
      const roll = String(doc.studentId).trim(), centre = allowed.get(roll);
      const lookup = questions.get(doc.testId);
      const identity = roll + ':' + doc.testId;
      if (!centre || !lookup?.size || seen.has(identity)) continue;
      seen.add(identity);
      const marks = doc.marks instanceof Map ? Object.fromEntries(doc.marks) : doc.marks || {};
      const metrics = {};
      for (const [question, subject] of lookup) {
        const rawMark = marks[question];
        if (rawMark === null || rawMark === undefined || String(rawMark).trim() === '' || !Number.isFinite(Number(rawMark))) continue;
        const metric = metrics[subject] ||= { attempted: 0, correct: 0 };
        const value = Number(rawMark);
        if (value !== 0) metric.attempted++;
        if (value > 0) metric.correct++;
      }
      if (!Object.keys(metrics).length) continue;
      metrics.Total = Object.values(metrics).reduce((sum, m) => ({ attempted: sum.attempted + m.attempted, correct: sum.correct + m.correct }), { attempted: 0, correct: 0 });
      const centreMetrics = byCentre[centre] ||= {};
      for (const [subject, metric] of Object.entries(metrics)) { add(centreMetrics, subject, metric); add(overall, subject, metric); }
    }
    const finish = group => Object.fromEntries(Object.entries(group).flatMap(([subject, m]) => [
      [subject + '_Attempted', m.attempted / m.records],
      [subject + '_Accuracy', m.attempted ? m.correct / m.attempted * 100 : 0],
    ]));
    return { testKey, centres: Object.fromEntries(Object.entries(byCentre).map(([centre, metrics]) => [centre, finish(metrics)])), overall: finish(overall) };
}
