import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_code = '<SectionTitle Icon={PieChartIcon} color="#3b82f6">Centre Distribution</SectionTitle>'
new_code = '<SectionTitle Icon={PieChartIcon} color="#f59e0b">Centre Distribution</SectionTitle>'

if old_code in content:
    content = content.replace(old_code, new_code)
else:
    print("Code not found!")

with open(filepath, 'w') as f:
    f.write(content)
print("Title color patched successfully.")
