import { parseTestColumn, flatToNested } from './testColumns.js';

const fail = message => { throw Object.assign(new Error(message), { statusCode: 400 }); };
const norm = v => String(v ?? '').trim().replace(/\.0+$/, '').toUpperCase();
const subjects = new Set(['Physics', 'Chemistry', 'Math', 'Biology', 'Botany', 'Zoology']);

// Validate the entire file before any write. A complete import cannot skip bad rows.
export function validateCompleteTestImport({ testKey, stream, marks }, profiles) {
  if (!/^[A-Za-z0-9][A-Za-z0-9() -]*$/.test(testKey || '')) fail('Select one base test, such as MT01, for replacement.');
  if (!['JEE', 'NEET'].includes(stream)) fail('Select a stream.');
  if (!Array.isArray(marks) || !marks.length) fail('The complete test file is empty.');
  const seen = new Set();
  return marks.map((row, index) => {
    const roll = norm(row.rollKey), center = norm(row.centerCode);
    if (!roll || !center) fail(`Row ${index + 1}: roll number and centre are required.`);
    if (seen.has(roll)) fail(`Duplicate roll number: ${roll}.`);
    seen.add(roll);
    const matches = profiles.filter(p => norm(p.ROLL_KEY) === roll);
    if (matches.length !== 1 || norm(matches[0].centerCode) !== center || norm(matches[0].stream || 'JEE') !== stream) {
      fail(`Roll ${roll}: a unique matching student profile, centre and stream are required.`);
    }
    const entries = Object.entries(row.scores || {});
    if (!entries.length || entries.some(([key]) => parseTestColumn(key).testName !== testKey)) fail(`Roll ${roll}: the file must contain only ${testKey}.`);
    const nested = flatToNested(row.scores).tests[testKey];
    if (!nested || !Object.hasOwn(nested, 'total')) fail(`Roll ${roll}: total marks are required for a complete test import.`);
    const scores = {};
    for (const [subject, value] of Object.entries(nested)) {
      if (subject !== 'total' && !subjects.has(subject)) fail(`Roll ${roll}: unsupported marks column ${subject}.`);
      if (typeof value === 'boolean' || value === null || String(value).trim() === '' || !Number.isFinite(Number(value))) fail(`Roll ${roll}: ${subject} must be numeric (zero and negative marks are allowed).`);
      scores[subject] = Number(value);
    }
    const required = stream === 'JEE' ? ['Physics', 'Chemistry', 'Math'] : ['Physics', 'Chemistry', ...(Object.hasOwn(scores, 'Biology') ? ['Biology'] : ['Botany', 'Zoology'])];
    if (required.every(s => Object.hasOwn(scores, s)) && Math.abs(required.reduce((sum, s) => sum + scores[s], 0) - scores.total) > 0.001) fail(`Roll ${roll}: subject marks do not add up to the total.`);
    return { roll, center, scores };
  });
}

// Clear only this test, including legacy flat columns. Keep every other test intact.
export function replacementUpdate(doc, testKey, scores) {
  const unset = {};
  if (doc.tests && Object.hasOwn(doc.tests, testKey) && !scores) unset[`tests.${testKey}`] = '';
  const metadata = new Set(['_id', '__v', 'ROLL_KEY', 'rollKey', 'centerCode', 'centreCode', 'stream', 'tests', 'createdAt', 'updatedAt']);
  for (const key of Object.keys(doc)) {
    if (!metadata.has(key) && parseTestColumn(key).testName === testKey) unset[key] = '';
  }
  const update = {};
  if (Object.keys(unset).length) update.$unset = unset;
  if (scores) update.$set = { [`tests.${testKey}`]: scores };
  return update;
}
