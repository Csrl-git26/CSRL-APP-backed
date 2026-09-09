import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_logic = """  const subjects = ['Physics', 'Chemistry', 'Math', 'Mathematics', 'Biology', 'Botany', 'Zoology'];
  const subjectScores = [];
  if (rawScores) {
    subjects.forEach(sub => {
      if (rawScores[sub] !== undefined && rawScores[sub] !== null) {
        let abbr = sub.substring(0, 3);
        if (sub === 'Mathematics') abbr = 'Mat';
        subjectScores.push(`${abbr}: ${rawScores[sub]}`);
      }
    });
  }"""

new_logic = """  const subjects = ['Physics', 'Chemistry', 'Math', 'Mathematics', 'Biology', 'Botany', 'Zoology'];
  const subjectScores = [];
  if (rawScores) {
    subjects.forEach(sub => {
      // Find a key in rawScores that matches the subject (e.g. exactly 'Physics' or ends with '_Physics')
      const matchedKey = Object.keys(rawScores).find(k => k === sub || k.toLowerCase().endsWith('_' + sub.toLowerCase()));
      if (matchedKey && rawScores[matchedKey] !== undefined && rawScores[matchedKey] !== null && rawScores[matchedKey] !== '') {
        let abbr = sub.substring(0, 3);
        if (sub === 'Mathematics') abbr = 'Mat';
        subjectScores.push(`${abbr}: ${rawScores[matchedKey]}`);
      }
    });
  }"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched InsightsDashboard.jsx for single test subject marks")
else:
    print("WARNING: Could not find logic to replace in InsightsDashboard.jsx")
