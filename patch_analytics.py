import re
import sys

with open('/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js', 'r') as f:
    content = f.read()

# We need to insert getScore helper at the top of computeTestInsights
# And replace subjectCols usage.

def patch():
    global content
    
    # 1. We replace subjectCols logic
    old_subj_logic = """  const subjectCols = (testColumns || []).filter((col) => {
    const p = parseTestColumn(col);
    return !p.isTotal && validTestKeys.includes(p.testName);
  });

  let subjects = [...new Set(subjectCols.map((c) => parseTestColumn(c).subject))];
  if (options.stream === 'NEET') {
    subjects = subjects.filter(s => !['Math', 'Mathematics'].includes(s));
  } else if (options.stream === 'JEE') {
    subjects = subjects.filter(s => !['Biology', 'Botany', 'Zoology'].includes(s));
  }"""

    new_subj_logic = """  const getScoreForDoc = (doc, sub, validTestKeys) => {
    if (!doc) return null;
    const rKeys = Object.keys(doc);
    let k = null;
    for (const rk of rKeys) {
        const pcol = parseTestColumn(rk);
        if (validTestKeys.includes(pcol.testName) && pcol.subject === sub) {
        k = rk;
        break;
        }
    }
    if (!k) {
        k = rKeys.find(rk => {
        const rkUpper = rk.toUpperCase();
        const subUpper = sub.toUpperCase();
        if (rkUpper === subUpper || (rkUpper === "PHY" && sub === "Physics") || (rkUpper === "CHEM" && sub === "Chemistry") || (rkUpper === "BIO" && sub === "Biology") || (rkUpper === "BOT" && sub === "Botany") || (rkUpper === "ZOO" && sub === "Zoology") || (rkUpper === "MAT" && sub === "Math") || (rkUpper === "MATHS" && sub === "Math") || (rkUpper === "MATHEMATICS" && sub === "Math")) return true;
        return rk.toLowerCase().endsWith("_" + sub.toLowerCase()) || (rkUpper.endsWith("_PHY") && sub === "Physics") || (rkUpper.endsWith("_CHEM") && sub === "Chemistry") || (rkUpper.endsWith("_BIO") && sub === "Biology") || (rkUpper.endsWith("_BOT") && sub === "Botany") || (rkUpper.endsWith("_ZOO") && sub === "Zoology") || (rkUpper.endsWith("_MAT") && sub === "Math") || (rkUpper.endsWith("_MATHS") && sub === "Math");
        });
    }
    if (k && !isNaN(Number(doc[k]))) {
        let val = Number(doc[k]);
        return val > 0 ? val : 0;
    }
    return null;
  };

  let subjectsSet = new Set();
  const allSubjs = ['Physics', 'Chemistry', 'Math', 'Biology', 'Botany', 'Zoology'];
  for (const sub of allSubjs) {
     if (options.stream === 'JEE' && ['Biology', 'Botany', 'Zoology'].includes(sub)) continue;
     if (options.stream === 'NEET' && ['Math', 'Mathematics'].includes(sub)) continue;
     for (const p of profiles) {
        const doc = tests.find((t) => t.ROLL_KEY === p.ROLL_KEY);
        if (doc && getScoreForDoc(doc, sub, validTestKeys) !== null) {
            subjectsSet.add(sub);
            break;
        }
     }
  }
  let subjects = Array.from(subjectsSet);"""

    content = content.replace(old_subj_logic, new_subj_logic)

    # 2. Replace subjectMins logic
    old_min_1 = """      subjectCols.forEach((col) => {
        const subj = parseTestColumn(col).subject;
        subjectMins[subj] = 30; // 30 marks per subject for all categories
      });"""
    new_min_1 = """      subjects.forEach((subj) => {
        subjectMins[subj] = 30; // 30 marks per subject for all categories
      });"""
    content = content.replace(old_min_1, new_min_1)

    old_min_2 = """      subjectCols.forEach((col) => {
        const subj = parseTestColumn(col).subject;
        subjectMins[subj] = maxForSubject(stream, subj) * subRatio;
      });"""
    new_min_2 = """      subjects.forEach((subj) => {
        subjectMins[subj] = maxForSubject(stream, subj) * subRatio;
      });"""
    content = content.replace(old_min_2, new_min_2)

    # 3. Replace subjectScores logic
    old_scores = """    const subjectScores = {};
    const subjectCounts = {};
    subjectCols.forEach((col) => {
      const subj = parseTestColumn(col).subject;
      const m = doc ? numericScore(doc[col]) : null;
      if (m !== null) {
        subjectScores[subj] = (subjectScores[subj] || 0) + m;
        subjectCounts[subj] = (subjectCounts[subj] || 0) + 1;
      }
    });"""
    new_scores = """    const subjectScores = {};
    const subjectCounts = {};
    subjects.forEach((subj) => {
      const m = getScoreForDoc(doc, subj, validTestKeys);
      if (m !== null) {
        subjectScores[subj] = (subjectScores[subj] || 0) + m;
        subjectCounts[subj] = (subjectCounts[subj] || 0) + 1;
      }
    });"""
    content = content.replace(old_scores, new_scores)

    # 4. Remove old getScore in the later part of the file
    old_getscore_block = """    const rKeys = Object.keys(doc);
    const getScore = (sub) => {
       let k = null;
       for (const rk of rKeys) {
         const pcol = parseTestColumn(rk);
         if (validTestKeys.includes(pcol.testName) && pcol.subject === sub) {
            k = rk;
            break;
         }
       }
       if (!k) {
         k = rKeys.find(rk => {
            const rkUpper = rk.toUpperCase();
            const subUpper = sub.toUpperCase();
            if (rkUpper === subUpper || (rkUpper === "PHY" && sub === "Physics") || (rkUpper === "CHEM" && sub === "Chemistry") || (rkUpper === "BIO" && sub === "Biology") || (rkUpper === "BOT" && sub === "Botany") || (rkUpper === "ZOO" && sub === "Zoology") || (rkUpper === "MAT" && sub === "Math") || (rkUpper === "MATHS" && sub === "Math") || (rkUpper === "MATHEMATICS" && sub === "Math")) return true;
            return rk.toLowerCase().endsWith("_" + sub.toLowerCase()) || (rkUpper.endsWith("_PHY") && sub === "Physics") || (rkUpper.endsWith("_CHEM") && sub === "Chemistry") || (rkUpper.endsWith("_BIO") && sub === "Biology") || (rkUpper.endsWith("_BOT") && sub === "Botany") || (rkUpper.endsWith("_ZOO") && sub === "Zoology") || (rkUpper.endsWith("_MAT") && sub === "Math") || (rkUpper.endsWith("_MATHS") && sub === "Math");
         });
       }
       if (k && !isNaN(Number(doc[k]))) {
           let val = Number(doc[k]);
           return val > 0 ? val : 0;
       }
       return null;
    };"""
    new_getscore_block = """    const getScore = (sub) => getScoreForDoc(doc, sub, validTestKeys);"""
    content = content.replace(old_getscore_block, new_getscore_block)

    with open('/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js', 'w') as f:
        f.write(content)
        
patch()
print("Done")
