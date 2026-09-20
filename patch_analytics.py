import os

filepath = '/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js'
with open(filepath, 'r') as f:
    content = f.read()

# Fix 1: rankCentresByTest to sum subjects if total is missing
old_centre_rank = """    testKeys.forEach(key => {
      const mark = numericScore(doc[key]);
      if (mark === null) return;
      centreAgg[code].sum   += mark;
      centreAgg[code].count += 1;"""

new_centre_rank = """    testKeys.forEach(key => {
      let mark = numericScore(doc[key]);
      
      if (mark === null) {
        let subjectSum = 0;
        let hasSubject = false;
        const subjects = ["Physics", "Chemistry", "Math", "Mathematics", "Biology", "Botany", "Zoology"];
        subjects.forEach(sub => {
          let sm = null;
          const rKeys = Object.keys(doc);
          const strictKey = rKeys.find(tk => tk.startsWith(key) && tk.toLowerCase().includes(sub.toLowerCase()));
          if (strictKey) {
            sm = numericScore(doc[strictKey]);
          } else {
            const fallbackKey = rKeys.find(tk => tk.toLowerCase() === sub.toLowerCase());
            if (fallbackKey) sm = numericScore(doc[fallbackKey]);
          }
          if (sm !== null) { subjectSum += sm; hasSubject = true; }
        });
        if (hasSubject) mark = subjectSum;
      }
      
      if (mark === null) return;
      centreAgg[code].sum   += mark;
      centreAgg[code].count += 1;"""

content = content.replace(old_centre_rank, new_centre_rank)

# Fix 2: Also computeTestInsights fallback for Total
old_insights_sum = """    testKeys.forEach(key => {
      const mark = numericScore(testDoc[key]);
      if (mark !== null) {
        hasAppeared = true;
        totalSum += mark;"""

new_insights_sum = """    testKeys.forEach(key => {
      let mark = numericScore(testDoc[key]);
      if (mark === null) {
        let subjectSum = 0;
        let hasSubject = false;
        const subjects = ["Physics", "Chemistry", "Math", "Mathematics", "Biology", "Botany", "Zoology"];
        subjects.forEach(sub => {
          let sm = null;
          const rKeys = Object.keys(testDoc);
          const strictKey = rKeys.find(tk => tk.startsWith(key) && tk.toLowerCase().includes(sub.toLowerCase()));
          if (strictKey) {
            sm = numericScore(testDoc[strictKey]);
          } else {
            const fallbackKey = rKeys.find(tk => tk.toLowerCase() === sub.toLowerCase());
            if (fallbackKey) sm = numericScore(testDoc[fallbackKey]);
          }
          if (sm !== null) { subjectSum += sm; hasSubject = true; }
        });
        if (hasSubject) mark = subjectSum;
      }
      if (mark !== null) {
        hasAppeared = true;
        totalSum += mark;"""

content = content.replace(old_insights_sum, new_insights_sum)


with open(filepath, 'w') as f:
    f.write(content)

print("analyticsService.js patched successfully.")
