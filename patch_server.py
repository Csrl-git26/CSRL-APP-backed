import re

with open('server.js', 'r') as f:
    content = f.read()

target = """    const finalChartData = enrichedChartData.map((row) => {
      const normRowName = (row.name || '').replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
      const wt = weakMap[normRowName];"""

replacement = """    const finalChartData = enrichedChartData.map((row) => {
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

      const wt = weakMap[normRowName];"""

if target in content:
    content = content.replace(target, replacement)
    with open('server.js', 'w') as f:
        f.write(content)
    print("Patched server.js")
else:
    print("Target not found")
