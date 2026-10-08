export function validateFacultyResults(input) {
  if (!Array.isArray(input) || !input.length || input.length > 10000) throw new Error('Provide between 1 and 10000 result rows.');
  const seen = new Set();
  return input.map((r, i) => {
    const text = k => String(r[k] ?? '').trim();
    const email = text('email').toLowerCase();
    const year = text('year'), test = text('test').toUpperCase(), subject = text('subject').toUpperCase();
    const name = text('name');
    if (!email.includes('@') || !name || !year || !test || !subject) throw new Error(`Row ${i + 1}: name, email, year, test and subject are required.`);
    const number = k => { if (r[k] === null || r[k] === undefined || r[k] === '') return null; const v = Number(r[k]); if (!Number.isFinite(v)) throw new Error(`Row ${i + 1}: invalid ${k}.`); return v; };
    const attempted = number('attempted'), correct = number('correct'), marks = number('marks'), maxMarks = number('maxMarks'), totalQuestions = number('totalQuestions');
    if ([attempted, correct].some(v => v !== null && (v < 0 || !Number.isInteger(v))) || (correct !== null && (attempted === null || correct > attempted))) throw new Error(`Row ${i + 1}: invalid attempted/correct counts.`);
    if (maxMarks !== null && (maxMarks <= 0 || marks > maxMarks)) throw new Error(`Row ${i + 1}: invalid maximum marks.`);
    if (totalQuestions !== null && (totalQuestions <= 0 || !Number.isInteger(totalQuestions) || attempted > totalQuestions)) throw new Error(`Row ${i + 1}: invalid total questions.`);
    const accuracy = attempted > 0 && correct !== null ? Math.round(correct / attempted * 10000) / 100 : null;
    const qualification = text('qualification').toUpperCase();
    if (qualification && !['QUALIFIED', 'NOT QUALIFIED'].includes(qualification)) throw new Error(`Row ${i + 1}: invalid qualification.`);
    const status = text('status').toUpperCase() || (marks !== null ? 'APPEARED' : 'MISSING');
    if (!['APPEARED','ABSENT','MEDICAL LEAVE','LEAVE','MISSING'].includes(status)) throw new Error(`Row ${i + 1}: invalid attendance status.`);
    if (status !== 'APPEARED' && (marks !== null || attempted !== null || correct !== null)) throw new Error(`Row ${i + 1}: leave/absent entries cannot contain scores.`);
    const key = JSON.stringify([year,email,test,subject]);
    if (seen.has(key)) throw new Error(`Row ${i + 1}: duplicate faculty/test/subject.`); seen.add(key);
    const date = text('date');
    if (date && !/^\d{4}-\d{2}-\d{2}$/.test(date)) throw new Error(`Row ${i + 1}: use YYYY-MM-DD for dates.`);
    const profile = Object.fromEntries(['facultyId','serialNumber','contact','projectManager','mentor','degree','college','passingYear','joiningDate'].map(key => [key,text(key)]));
    return { ...profile,year,email,name,test,subject,centres: text('centres').toUpperCase().split(/\s*(?:&|,|;)\s*/).filter(Boolean),attempted,correct,marks,maxMarks,totalQuestions,accuracy,qualification,status,date };
  });
}
