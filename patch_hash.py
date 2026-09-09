import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("`#${rank}`", "`${rank}`")
content = content.replace("`#${c.rank}`", "`${c.rank}`")

with open(filepath, 'w') as f:
    f.write(content)

print("Removed '#' from rank displays")
