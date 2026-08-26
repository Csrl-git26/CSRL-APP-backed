import sys

filepath = '/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Patch the qualified block
old_qualified = """    let qualified = total !== null && total >= overallMin;
    if (qualified) {
      for (const col of subjectCols) {
        const subj = parseTestColumn(col).subject;
        const m = numericScore(doc[col]);
        const smin = subjectMins[subj];
        if (m !== null && smin !== undefined && m < smin) qualified = false;
      }
    } else {
      qualified = false;
    }"""

new_qualified = """    let qualified = total !== null && total >= overallMin;
    if (qualified && stream !== 'JEE') {
      for (const col of subjectCols) {
        const subj = parseTestColumn(col).subject;
        const m = numericScore(doc[col]);
        const smin = subjectMins[subj];
        if (m !== null && smin !== undefined && m < smin) qualified = false;
      }
    } else if (!qualified) {
      qualified = false;
    }"""

# 2. Patch the notQualifiedBySubject counter block
old_counter = """      const smin = st.subjectMins[subj];
      if (m !== null && smin !== undefined && m < smin) {"""

new_counter = """      const smin = st.subjectMins[subj];
      if (m !== null && smin !== undefined && m <= smin) {"""

if old_qualified in content and old_counter in content:
    content = content.replace(old_qualified, new_qualified)
    content = content.replace(old_counter, new_counter)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched analyticsService.js successfully!")
else:
    print("Failed to find replacement blocks in analyticsService.js")
    if old_qualified not in content: print("Missing old_qualified")
    if old_counter not in content: print("Missing old_counter")

