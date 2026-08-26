import http from 'http';
http.get('http://localhost:5000/api/analytics/global-insights?testKey=FMT08', (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const parsed = JSON.parse(data);
    const firstStudent = parsed.insights.rankedStudents[0];
    console.log(Object.keys(firstStudent.rawScores || {}));
  });
}).on('error', (e) => {
  console.error(e);
});
