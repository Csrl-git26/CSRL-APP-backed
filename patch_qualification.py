import sys

filepath = '/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js'
with open(filepath, 'r') as f:
    content = f.read()

old_logic = """    const overallMin = stream === 'NEET' ? neetOverallMin : (caps.maxTotal * jeeOverallQualifyRatio);
    const subjectMins = {};
    const subRatio = stream === 'JEE' ? jeeSubjectQualifyRatio : neetSubjectQualifyRatio;
    subjectCols.forEach((col) => {
      const subj = parseTestColumn(col).subject;
      subjectMins[subj] = maxForSubject(stream, subj) * subRatio;
    });"""

new_logic = """    let overallMin;
    const subjectMins = {};
    if (stream === 'JEE') {
      const cat = (p.CATEGORY || '').toUpperCase().trim();
      if (cat.includes('PWD')) overallMin = 30;
      else if (cat.includes('ST')) overallMin = 60;
      else if (cat.includes('SC')) overallMin = 65;
      else if (cat.includes('OBC')) overallMin = 85;
      else if (cat.includes('EWS')) overallMin = 90;
      else overallMin = 110; // GEN or default

      subjectCols.forEach((col) => {
        const subj = parseTestColumn(col).subject;
        subjectMins[subj] = 20; // 20 marks per subject for all categories
      });
    } else {
      overallMin = neetOverallMin;
      const subRatio = neetSubjectQualifyRatio;
      subjectCols.forEach((col) => {
        const subj = parseTestColumn(col).subject;
        subjectMins[subj] = maxForSubject(stream, subj) * subRatio;
      });
    }"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched analyticsService.js qualification logic successfully!")
else:
    print("Could not find the old logic block in analyticsService.js")
