import { parseTestColumn } from '../utils/testColumns.js';

const SUBJECTS = ['Total', 'Physics', 'Chemistry', 'Math', 'Botany', 'Zoology', 'Biology'];
const norm = v => String(v ?? '').trim().toUpperCase();
export function centerCode(v) {
  const c = norm(v);
  return ({ GAIL: 'KNP', OIL_INDIA: 'JDH', 'OIL INDIA': 'JDH' })[c] || c;
}
const roll = v => norm(v).replace(/\.0+$/, '');
const identity = r => `${centerCode(r.centerCode)}:${roll(r.ROLL_KEY)}`;
export function numberScore(v) {
  if (v === null || v === undefined || typeof v === 'boolean' || String(v).trim() === '') return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}
const rounded = n => n === null ? null : Math.round(n * 100) / 100;
const average = vs => vs.length ? vs.reduce((s, v) => s + v, 0) / vs.length : null;
const family = id => norm(id).match(/^[A-Z]+/)?.[0] || '';
const sequence = id => Number(String(id).match(/^[A-Z]+[\s-]*(\d+)/i)?.[1] ?? -1);
const display = v => v === null ? 'No recorded mark' : rounded(v);
function nameOf(p) {
  for (const alias of ['studentsname', 'studentname', 'name', 'fullname']) {
    const entry = Object.entries(p || {}).find(([k,v]) => k.toLowerCase().replace(/[^a-z]/g, '') === alias && typeof v === 'string' && v.trim());
    if (entry) return entry[1].trim();
  }
  return 'Name unavailable';
}

// Always enforce permissions before interpreting questions or sending metadata to AI.
export function scopeChatData(data, user, assignedCenters = []) {
  const role = user?.role;
  if (!['admin', 'centre', 'student'].includes(role)) throw Object.assign(new Error('This login cannot use academic chat.'), { status: 403 });
  const allowed = new Set(assignedCenters.map(centerCode));
  if (role === 'centre' && !allowed.size) throw Object.assign(new Error('Use a named centre login with assigned centre codes to access chat.'), { status: 403 });
  const permitted = r => role === 'admin' || (role === 'centre' ? allowed.has(centerCode(r.centerCode)) : centerCode(r.centerCode) === centerCode(user.centerCode) && roll(r.ROLL_KEY) === roll(user.id));
  return { ...data, profiles: (data.profiles || []).filter(permitted), tests: (data.tests || []).filter(permitted) };
}

export function makeCatalog(data, stream = 'JEE') {
  const profiles = new Map((data.profiles || []).map(p => [identity(p), p]));
  const rows = (data.tests || []).filter(r => {
    const p = profiles.get(identity(r));
    return norm(p?.stream || p?.STREAM || p?.Stream || r.stream || 'JEE') === stream;
  });
  const columns = new Map();
  const metadata = new Set(['ROLL_KEY', 'centerCode', 'centreCode', 'stream', '_id', '__v', 'createdAt', 'updatedAt', 'tests']);
  for (const r of rows) for (const col of Object.keys(r)) {
    if (metadata.has(col)) continue;
    const parsed = parseTestColumn(col);
    if (!SUBJECTS.includes(parsed.subject) || !/^[A-Za-z]+[\s-]*\d/.test(parsed.testName)) continue;
    if ((/^(MMT|NCT|NMT|NEET|NFT|MFT)/i.test(parsed.testName)) !== (stream === 'NEET')) continue;
    if (!columns.has(parsed.testName)) columns.set(parsed.testName, new Map());
    const subs = columns.get(parsed.testName);
    if (!subs.has(parsed.subject)) subs.set(parsed.subject, []);
    if (!subs.get(parsed.subject).includes(col)) subs.get(parsed.subject).push(col);
  }
  return { rows, profiles, columns, centers: [...new Set(rows.map(r => centerCode(r.centerCode)))].filter(Boolean).sort(), tests: [...columns.keys()].sort((a,b) => family(a).localeCompare(family(b)) || sequence(a)-sequence(b) || a.localeCompare(b)) };
}
function score(row, test, subject, cat) {
  const cols = cat.columns.get(test)?.get(subject) || [];
  for (const col of cols) {
    if (Object.hasOwn(row, col)) return numberScore(row[col]);
  }
  return null;
}
export function parseQuestion(question, catalog, context = {}) {
  const q = String(question).toLowerCase();
  const followUp = /^(show only|only|and |also |what about|और |सिर्फ)|\b(their|these|those)\b/.test(q);
  if (!followUp) context = {};
  const explicitCenters = catalog.centers.filter(c => new RegExp(`(^|[^a-z0-9])${c.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}([^a-z0-9]|$)`, 'i').test(question));
  let intent = /attention|weak|support|below|under|कमजोर|ध्यान/.test(q) ? 'attention' : /improv|positive|declin|trend|compare|performance|प्रदर्शन|सुधार|गिरावट/.test(q) ? 'trends' : /summary|average|औसत|सारांश/.test(q) ? 'summary' : /help|how|upload|मदद/.test(q) ? 'help' : null;
  if (/student|विद्यार्थी|छात्र/.test(q) && /progress|history|previous|प्रगति/.test(q)) intent = 'student_progress';
  if (followUp && context.intent && !/progress|summary|average|centre|center|केंद्र/.test(q)) intent = context.intent;
  if (/\broll\b|रोल/.test(q)) intent = 'student_progress';
  const subject = /physics|\bphy\b|भौतिक/.test(q) ? 'Physics' : /chem|रसायन/.test(q) ? 'Chemistry' : /math|गणित/.test(q) ? 'Math' : /botany|वनस्पति/.test(q) ? 'Botany' : /zoology|प्राणी/.test(q) ? 'Zoology' : /biology|जीव/.test(q) ? 'Biology' : /overall|total|कुल/.test(q) ? 'Total' : context.subject || 'Total';
  const series = norm(question.match(/\b(CMT|CAT|FMT|JCT|MT|PT|NCT|NMT|MMT|NFT|MFT)\b/i)?.[1] || context.series);
  const n = question.match(/(?:last|latest|पिछले)\s*(\d+)/i)?.[1];
  const threshold = question.match(/(?:below|under|less than)\s*(-?\d+(?:\.\d+)?)(?!\d)/i);
  const testIds = catalog.tests.filter(t => norm(question).includes(norm(t)));
  const rollMatch = question.match(/(?:roll|रोल)\s*[:#-]?\s*([a-z0-9_-]+)/i);
  return { intent: intent || (Object.keys(context).length && /only|show|their|these|also|सिर्फ|दिखा/.test(q) ? context.intent : 'unknown'), subject, centers: explicitCenters.length ? explicitCenters : /all cent|every cent|सभी केंद्र/.test(q) ? [] : context.centers || [], series, count: n ? Math.min(10, Math.max(1, Number(n))) : context.count || 3, direction: /declin|fall|गिरावट/.test(q) ? 'declining' : /improv|positive|सुधार/.test(q) ? 'improving' : context.direction || 'all', threshold: threshold && !/%|percent/.test(q) ? Number(threshold[1]) : context.threshold ?? null, testIds, roll: rollMatch?.[1] || context.roll || '' };
}
export function validatePlan(plan, cat) {
  if (!plan || typeof plan !== 'object' || !['attention','trends','summary','student_progress','help','unknown'].includes(plan.intent)) return null;
  if (!SUBJECTS.includes(plan.subject)) return null;
  if (!Array.isArray(plan.centers) || plan.centers.length > 10 || plan.centers.some(c => typeof c !== 'string' || !cat.centers.includes(centerCode(c)))) return null;
  if (typeof plan.series !== 'string' || plan.series && !/^[A-Z]{2,8}$/.test(plan.series)) return null;
  if (!Array.isArray(plan.testIds) || plan.testIds.length > 10 || plan.testIds.some(t => !cat.tests.includes(t))) return null;
  if (!Number.isInteger(plan.count) || plan.count < 1 || plan.count > 10) return null;
  if (!['all','improving','declining'].includes(plan.direction)) return null;
  if (plan.threshold !== null && (typeof plan.threshold !== 'number' || !Number.isFinite(plan.threshold) || plan.threshold < -1000 || plan.threshold > 1000)) return null;
  if (typeof plan.roll !== 'string' || plan.roll.length > 80) return null;
  return { intent: plan.intent, subject: plan.subject, centers: plan.centers.map(centerCode), series: plan.series, testIds: plan.testIds, count: plan.count, direction: plan.direction, threshold: plan.threshold, roll: plan.roll };
}
const reply = answer => ({ answer, columns: [], rows: [], sources: [], notes: [] });
export function analyzeChat(cat, plan, { role, stream, branch }) {
  if (plan.intent === 'help') return reply('Ask about student attention lists, centre averages, centre trends, or a student’s marks by roll number. For example: “KNP students needing attention in Physics in the last 3 CMT tests”. Choose the stream and branch above. I use recorded marks; I cannot establish the cause of a decline or assess teaching quality from marks alone.');
  if (plan.intent === 'unknown') return reply('I could not confidently match that question to available academic data. Please specify a centre, subject and test series. I can analyse attention lists, centre trends, averages and student progress; other requests are not yet supported.');
  if (role === 'student' && plan.intent !== 'student_progress') return reply('Your login can review your own marks. Ask “Show my student progress in Physics in the last 3 CMT tests”. Centre comparisons and other students’ names require an authorised staff login.');
  const baseRows = cat.rows.filter(r => !plan.centers.length || plan.centers.includes(centerCode(r.centerCode)));
  if (!baseRows.length) return reply('No accessible marks were found for this centre and stream. Check the selected stream or centre code.');
  if (plan.intent === 'attention' && !plan.centers.length && role !== 'student') return reply('Which centre should I check? Include its code, for example “KNP students needing attention in Physics”.');
  let tests = plan.testIds.length ? plan.testIds : cat.tests.filter(t => !plan.series || family(t) === plan.series);
  if (!plan.testIds.length && !plan.series) {
    const families = [...new Set(tests.map(family))];
    if (families.length !== 1) return reply(`Which test series should I use? Available: ${families.join(', ') || 'none'}. For example, add “last 3 CMT tests”.`);
  }
  if (new Set(tests.map(family)).size > 1) return reply('Please compare tests from the same series, such as CMT. Different test series can use different scoring scales.');
  tests = [...tests].sort((a,b) => sequence(a)-sequence(b) || a.localeCompare(b));
  if (!plan.testIds.length) tests = tests.slice(-plan.count);
  if (!tests.length) return reply('No matching tests are available in your permitted records and selected stream/branch.');
  if (tests.some(t => !cat.columns.get(t)?.has(plan.subject))) return reply(`The selected tests do not all contain ${plan.subject} marks. Choose another subject or test series.`);
  const notes = [
    `${stream}${stream === 'JEE' ? ' / ' + branch : ''}; ${plan.subject}; tests ordered by test number, oldest to newest. Test dates are not available here.`,
    'Marks are raw scores, not percentages. Difficulty and maximum-mark differences are not adjusted; compare only tests with the same scoring scale.',
    'Blank, absent and invalid marks are excluded, never counted as zero. Zero and negative marks are retained.'
  ];
  if (!plan.testIds.length && tests.length < plan.count) notes.push(`Only ${tests.length} matching tests are available (requested ${plan.count}).`);
  const sources = tests.map(t => ({ test: t, subject: plan.subject }));
  const profile = r => cat.profiles.get(identity(r));
  const values = r => tests.map(t => score(r,t,plan.subject,cat));
  const complete = v => v.every(x => x !== null);
  const changes = v => v.slice(1).map((x,i) => x-v[i]);
  const studentColumns = ['Student name','Roll number','Centre', ...tests, 'Reason / trend'];
  let rows = [], answer = '';
  if (plan.intent === 'attention') {
    const latest = tests.at(-1);
    const means = new Map([...new Set(baseRows.map(r => centerCode(r.centerCode)))].map(c => [c, average(baseRows.filter(r => centerCode(r.centerCode) === c).map(r => score(r,latest,plan.subject,cat)).filter(x => x !== null))]));
    let missing = 0;
    for (const r of baseRows) {
      const v = values(r), last = v.at(-1), reasons = [];
      if (last === null) { missing++; continue; }
      const threshold = plan.threshold ?? means.get(centerCode(r.centerCode));
      if (threshold !== null && last < threshold) reasons.push(plan.threshold === null ? `Below latest centre average (${rounded(threshold)} marks)` : `Below ${threshold} marks`);
      if (v.length >= 3 && complete(v) && changes(v).every(x => x < 0)) reasons.push('Declined at every comparison');
      if (plan.direction === 'declining' && !(v.length >= 2 && complete(v) && changes(v).every(x => x < 0))) continue;
      if (reasons.length || plan.direction === 'declining') rows.push([nameOf(profile(r)),roll(r.ROLL_KEY),centerCode(r.centerCode),...v.map(display), reasons.join('; ') || 'Marks declined']);
    }
    rows.sort((a,b) => Number(a[a.length-2])-Number(b[b.length-2]) || a[0].localeCompare(b[0]));
    answer = `${rows.length} student(s) match the attention criteria for ${plan.subject}. ${missing} student record(s) have no usable mark in ${latest} and are excluded from this list.`;
    notes.push(plan.threshold === null ? 'Screening rule: below the latest centre subject average OR a decline at every step across at least 3 tests. This is a review list, not a diagnosis of ability.' : `Screening rule: below ${plan.threshold} marks in the latest test OR a decline at every step across at least 3 tests.`);
    if (plan.direction === 'declining') notes.push('Additional filter: decline at every step across the selected tests.');
    notes.push('Suggested follow-up: review the answer sheets, arrange focused practice, and check the next result. Topic weaknesses require question-wise data.');
  } else if (plan.intent === 'student_progress') {
    if (role !== 'student' && !plan.roll) return reply('Please provide the student’s roll number and centre, for example “Student progress roll KNP001 at KNP in Physics, last 3 CMT tests”.');
    const matches = baseRows.filter(r => role === 'student' || roll(r.ROLL_KEY) === roll(plan.roll));
    if (matches.length > 1) return reply('More than one record matches this roll number. Please specify the centre.');
    rows = matches.map(r => { const v = values(r); return [nameOf(profile(r)),roll(r.ROLL_KEY),centerCode(r.centerCode),...v.map(display), complete(v) && v.length > 1 ? `${rounded(v.at(-1)-v[0])} marks from first to last` : 'Insufficient recorded marks for a trend']; });
    answer = rows.length ? 'Here are the student’s recorded marks, oldest to newest.' : 'No student record matches that roll number in your permitted data.';
  } else {
    if (plan.intent === 'trends' && tests.length < 2) return reply('At least two matching tests are needed to calculate a change.');
    const centers = [...new Set(baseRows.map(r => centerCode(r.centerCode)))].sort();
    let excluded = 0;
    for (const c of centers) {
      const group = baseRows.filter(r => centerCode(r.centerCode) === c);
      // Same cohort in every test prevents participation changes masquerading as progress.
      const matched = group.filter(r => complete(values(r)));
      if (!matched.length) { excluded++; continue; }
      const avgs = tests.map(t => average(matched.map(r => score(r,t,plan.subject,cat))));
      const deltas = changes(avgs);
      if (plan.direction === 'improving' && !(deltas.length && deltas.every(v => v > 0))) continue;
      if (plan.direction === 'declining' && !(deltas.length && deltas.every(v => v < 0))) continue;
      rows.push([c, matched.length, ...avgs.map(rounded), avgs.length > 1 ? rounded(avgs.at(-1)-avgs[0]) : '—', tests.map(t => `${t}: ${group.filter(r => score(r,t,plan.subject,cat) !== null).length}`).join('; ')]);
    }
    rows.sort((a,b) => typeof b[b.length-2] === 'number' ? b[b.length-2]-a[a.length-2] : a[0].localeCompare(b[0]));
    answer = `${rows.length} centre(s) match this comparison. Averages use only students with recorded marks in every selected test.`;
    notes.push(`${excluded} centre(s) excluded because no students had marks in all selected tests. “Recorded count” shows all valid marks per test; the averages use the common cohort only.`);
    if (tests.length === 2) notes.push('Two tests show one change. At least three tests are needed to check repeated improvement or decline.');
    return { answer, columns: ['Centre','Students compared',...tests,'Change in marks','Recorded count'], rows: rows.slice(0,200), totalRows: rows.length, sources, notes };
  }
  return { answer, columns: studentColumns, rows: rows.slice(0,200), totalRows: rows.length, sources, notes };
}

// Match only standalone conversation; greetings before a data question must not hide it.
export function conversationReply(question, role) {
  const q = question.trim().toLowerCase().replace(/[!?.।,]+/g, ' ').replace(/\s+/g, ' ').trim();
  const greeting = /^(?:h+i+|h+e+l+o+|h+l+o+|hey+|hai|namaste|namaskar|नमस्ते|नमस्कार|good morning|good afternoon|good evening)(?: pragati| प्रगति| bot)?$/u.test(q);
  const help = /^(?:help|help me|what can you do|how can you help me|who are you|मदद|आप क्या कर सकते हैं)$/u.test(q);
  const thanks = /^(?:thanks|thank you|thankyou|thank u|धन्यवाद|शुक्रिया)$/u.test(q);
  if (!greeting && !help && !thanks) return null;
  const hindi = /[\u0900-\u097f]/u.test(q);
  const examples = role === 'student'
    ? (hindi ? 'पूछें: “पिछले 3 CMT टेस्ट में मेरी Physics की प्रगति दिखाएँ।”' : 'Try: “Show my student progress in Physics in the last 3 CMT tests.”')
    : (hindi ? 'आप पूछ सकते हैं:\n• पिछले 2 CMT टेस्ट में किन केंद्रों का औसत बढ़ा?\n• KNP केंद्र में Physics में किन छात्रों को विशेष ध्यान चाहिए?\n• DEL केंद्र का CMT02 औसत कितना है?' : 'You can ask:\n• Which centres improved in the last 2 CMT tests?\n• Which KNP students need attention in Physics?\n• What is the DEL centre average in CMT02?');
  return `${thanks ? (hindi ? 'आपका स्वागत है!' : "You're welcome!") : (hindi ? 'नमस्ते! मैं आपके पोर्टल के शैक्षणिक डेटा को आसान भाषा में समझने में मदद कर सकती हूँ।' : "Hello! I can help you understand your portal’s academic data in simple language.")}\n\n${examples}`;
}
