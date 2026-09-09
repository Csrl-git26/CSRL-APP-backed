import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("innerRadius={45}", "innerRadius={35}")
content = content.replace("outerRadius={65}", "outerRadius={55}")
content = content.replace(
    "const radius = outerRadius + 12 + (index % 2 === 0 ? 0 : 14);",
    "const radius = outerRadius + 10 + (index % 2 === 0 ? 0 : 12);"
)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated PieChart radii to prevent label cropping")
