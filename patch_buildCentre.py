import re

with open('/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js', 'r') as f:
    content = f.read()

old_build_loop = """    ['Physics', 'Chemistry', 'Math', 'Biology'].forEach(sub => {
      const sum = agg.subjectSums[sub];
      const count = agg.subjectCounts[sub];
      row[sub] = (count > 0) ? Math.round(sum / count) : null;
    });"""
new_build_loop = """    ['Physics', 'Chemistry', 'Math', 'Biology', 'Botany', 'Zoology'].forEach(sub => {
      const sum = agg.subjectSums[sub];
      const count = agg.subjectCounts[sub];
      row[sub] = (count > 0) ? Math.round(sum / count) : null;
    });"""
content = content.replace(old_build_loop, new_build_loop)

with open('/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js', 'w') as f:
    f.write(content)
print("Done buildCentreChartData")
