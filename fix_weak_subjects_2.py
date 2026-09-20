import os
import re

filepath = "/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx"
with open(filepath, "r") as f:
    content = f.read()

# Instead of exact match, let's use regex to replace the IIFE inside the {(() => { ... })()} block
pattern = r"\{\(\(\) => \{\n\s*if \(\!overallWeakSubjects\).*?return weakest.*?None Flagged';\n\s*\}\)\(\)\}"

new_logic = """{(() => {
                  if (!overallWeakTopicsData || !overallWeakTopicsData.subjectWise) return 'Loading...';
                  const weakest = [];
                  const subjectWise = overallWeakTopicsData.subjectWise;
                  Object.keys(subjectWise).forEach(sub => {
                    const formatSub = sub.charAt(0) + sub.slice(1).toLowerCase();
                    if (subjectWise[sub]?.weak?.length > 0) weakest.push(formatSub === 'Mathematics' ? 'Math' : formatSub);
                  });
                  if (weakest.length === 0) {
                    Object.keys(subjectWise).forEach(sub => {
                      const formatSub = sub.charAt(0) + sub.slice(1).toLowerCase();
                      if (subjectWise[sub]?.moderate?.length > 0) weakest.push(`${formatSub === 'Mathematics' ? 'Math' : formatSub} (Medium)`);
                    });
                  }
                  return weakest.length > 0 ? weakest.join(', ') : 'None Flagged';
                })()}"""

content_new = re.sub(pattern, new_logic, content, flags=re.DOTALL)
if content != content_new:
    print("Fixed StudentProfileView.jsx")
    with open(filepath, "w") as f:
        f.write(content_new)
else:
    print("Could not find logic in StudentProfileView.jsx")

