import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace(
    'value={centreBoard.length} label="Centres Appeared"',
    'value={centreBoard.length} label="Active Centres"'
)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated label back to Active Centres")
