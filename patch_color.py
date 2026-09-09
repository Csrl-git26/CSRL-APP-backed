import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace(
    "color: c.qualRate < 80 ? '#dc2626' : '#16a34a'",
    "color: isAlert ? '#dc2626' : '#1a4fa0'"
)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated qualification text color to match average score color")
