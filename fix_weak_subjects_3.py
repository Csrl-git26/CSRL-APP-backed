import os
import re

filepath = "/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx"
with open(filepath, "r") as f:
    content = f.read()

pattern = r"\{\(\(\) => \{\n\s*if \(\!overallWeakSubjects\).*?return weakest.*?None Flagged';\n\s*\}\)\(\)\}"

new_logic = """{(() => {
              if (!overallWeakTopicsData || !overallWeakTopicsData.subjectWise) return 'N/A';
              const weakest = [];
              const subjectWise = overallWeakTopicsData.subjectWise;
              Object.keys(subjectWise).forEach(sub => {
                const formatSub = sub.charAt(0) + sub.slice(1).toLowerCase();
                if (subjectWise[sub]?.weak?.length > 0) weakest.push(formatSub);
              });
              if (weakest.length === 0) {
                Object.keys(subjectWise).forEach(sub => {
                  const formatSub = sub.charAt(0) + sub.slice(1).toLowerCase();
                  if (subjectWise[sub]?.moderate?.length > 0) weakest.push(`${formatSub} (Med)`);
                });
              }
              return weakest.length > 0 ? weakest.join(', ') : 'None Flagged';
            })()}"""

content_new = re.sub(pattern, new_logic, content, flags=re.DOTALL)
if content != content_new:
    print("Fixed StudentReportCard.jsx")
    with open(filepath, "w") as f:
        f.write(content_new)
else:
    print("Could not find logic in StudentReportCard.jsx")

