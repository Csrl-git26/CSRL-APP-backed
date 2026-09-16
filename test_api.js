const fs = require('fs');
const { computeTestInsights } = require('./services/analyticsService.js');

(async () => {
  const parseCSV = (content) => {
    const rows = content.trim().split('\n');
    const headers = rows[0].split(',').map(h => h.trim());
    return rows.slice(1).map(row => {
      const values = row.split(',').map(v => v.trim());
      const obj = {};
      headers.forEach((h, i) => obj[h] = values[i]);
      return obj;
    });
  };

  const profRaw = fs.readFileSync('./uploads/studentProfile.csv', 'utf8');
  const profiles = parseCSV(profRaw);

  const testRaw = fs.readFileSync('./uploads/testHistory.csv', 'utf8');
  const tests = parseCSV(testRaw);

  const testKey = "MMT01,MMT02"; // From screenshot
  const testColumns = Object.keys(tests[0]).filter(k => k.startsWith('MMT01') || k.startsWith('MMT02'));

  const options = { stream: 'NEET' };
  
  const insights = computeTestInsights(profiles, tests, testKey, testColumns, options);

  console.log("SUBJECTS:", insights.subjects);
  console.log("SUBJECT TOP STUDENTS:", JSON.stringify(insights.subjectTopStudents, null, 2));
  console.log("NOT QUALIFIED BY SUBJECT:", Object.keys(insights.notQualifiedBySubject || {}));
})();
