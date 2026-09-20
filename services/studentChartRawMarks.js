// Include uploaded marks even when the legacy TestScore row has not been populated.
export function enrichStudentChartFromRawMarks(rows, rawMarks, topicMaps, stream) {
  const normalize = value => String(value || '').replace(/[^a-z0-9]/gi, '').toUpperCase();
  const subjects = { PHYSICS: 'Physics', CHEMISTRY: 'Chemistry', MATHEMATICS: 'Math', MATH: 'Math', BOTANY: 'Botany', ZOOLOGY: 'Zoology', BIOLOGY: 'Biology' };
  for (const doc of rawMarks) {
    const name = String(doc.testId || '').trim();
    if (!name || (/^(MMT|NCT|NMT|NEET)/i.test(name) !== (stream === 'NEET'))) continue;
    const map = topicMaps.find(t => t.testId === doc.testId);
    if (!map) continue;
    const questions = new Map();
    for (const topic of map.topics || []) {
      const subject = subjects[String(topic.subject || '').trim().toUpperCase()];
      if (!subject || (stream === 'NEET' ? subject === 'Math' : ['Botany', 'Zoology', 'Biology'].includes(subject))) continue;
      for (const q of topic.questions || []) questions.set(q, subject);
    }
    if (!questions.size) continue;
    let row = rows.find(r => normalize(r.name) === normalize(name));
    if (!row) { row = { name }; rows.push(row); }
    const marks = doc.marks instanceof Map ? Object.fromEntries(doc.marks) : (doc.marks || {});
    const metrics = {};
    for (const [q, subject] of questions) {
      const m = metrics[subject] ||= { score: 0, present: 0, attempted: 0, correct: 0 };
      const raw = marks[q];
      if (raw === null || raw === undefined || raw === '' || !Number.isFinite(Number(raw))) continue;
      const value = Number(raw);
      m.score += value; m.present++;
      if (value !== 0) m.attempted++;
      if (value > 0) m.correct++;
    }
    let total = 0, present = 0, attempted = 0, correct = 0;
    for (const [subject, m] of Object.entries(metrics)) {
      if (row[subject] == null || row[subject] === 'Absent') row[subject] = m.present ? m.score : 'Absent';
      row[`${subject}_Attempted`] = m.attempted;
      row[`${subject}_Correct`] = m.correct;
      row[`${subject}_Accuracy`] = m.attempted ? Math.round(m.correct / m.attempted * 100) : 0;
      total += m.score; present += m.present; attempted += m.attempted; correct += m.correct;
    }
    if (row.Total == null || row.Total === 'Absent') row.Total = present ? total : 'Absent';
    row.Total_Attempted = attempted;
    row.Total_Correct = correct;
    row.Total_Accuracy = attempted ? Math.round(correct / attempted * 100) : 0;
  }
  return rows;
}
