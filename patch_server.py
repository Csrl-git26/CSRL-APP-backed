import os
import re

filepath = '/Users/surya/Desktop/CSRL-APP-backed/server.js'
with open(filepath, 'r') as f:
    content = f.read()

# Fix 1: In app.get('/api/analytics/centre-chart', ...)
# Change hardcoded ['Physics', 'Chemistry', 'Math'] to use stream logic.
old_chart = """      ['Physics', 'Chemistry', 'Math'].forEach(sub => {
        const validCentres = insights.centreRows.filter(r => r.subjectAvgs[sub] !== null && r.subjectAvgs[sub] !== undefined);
        if (validCentres.some(r => r.code === centerCode)) {
          validCentres.sort((a, b) => b.subjectAvgs[sub] - a.subjectAvgs[sub]);
          row[`${sub}_Rank`] = validCentres.findIndex(r => r.code === centerCode) + 1;
        }
      });"""

new_chart = """      const subjects = stream === 'NEET' ? ['Physics', 'Chemistry', 'Botany', 'Zoology', 'Biology'] : ['Physics', 'Chemistry', 'Math', 'Mathematics'];
      subjects.forEach(sub => {
        const validCentres = insights.centreRows.filter(r => r.subjectAvgs[sub] !== null && r.subjectAvgs[sub] !== undefined);
        if (validCentres.some(r => r.code === centerCode)) {
          validCentres.sort((a, b) => b.subjectAvgs[sub] - a.subjectAvgs[sub]);
          row[`${sub}_Rank`] = validCentres.findIndex(r => r.code === centerCode) + 1;
        }
      });"""

content = content.replace(old_chart, new_chart)

# Fix 2: rankStudentsByTest missing Botany due to strict tk.startsWith(k)
old_student_rank = """          subjects.forEach(sub => {
            const subKey = Object.keys(testDoc).find(tk => tk.startsWith(k) && tk.toLowerCase().includes(sub.toLowerCase()));
            if (subKey) {
              const sm = numericScore(testDoc[subKey]);
              if (sm !== null) { subjectSum += sm; hasSubject = true; }
            }
          });"""

new_student_rank = """          subjects.forEach(sub => {
            let sm = null;
            const keys = Object.keys(testDoc);
            const strictKey = keys.find(tk => tk.startsWith(k) && tk.toLowerCase().includes(sub.toLowerCase()));
            if (strictKey) {
              sm = numericScore(testDoc[strictKey]);
            } else {
              const fallbackKey = keys.find(tk => tk.toLowerCase() === sub.toLowerCase());
              if (fallbackKey) sm = numericScore(testDoc[fallbackKey]);
            }
            if (sm !== null) { subjectSum += sm; hasSubject = true; }
          });"""

content = content.replace(old_student_rank, new_student_rank)

with open(filepath, 'w') as f:
    f.write(content)

print("server.js patched successfully.")
