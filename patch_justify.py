import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# For Top 5 Students
content = content.replace(
    "border:'1px solid #e8f0fc', height: '100%', display: 'flex', flexDirection: 'column' }}>",
    "border:'1px solid #e8f0fc', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>"
)

# For Top/Bottom Centres
content = content.replace(
    "border:'1px solid #e2e8f0', height: '100%', display: 'flex', flexDirection: 'column' }}>",
    "border:'1px solid #e2e8f0', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>"
)

# For Centre Distribution (Pie Chart)
content = content.replace(
    "border:'1px solid #e2e8f0', display: 'flex', flexDirection: 'column', height: '100%' }}>",
    "border:'1px solid #e2e8f0', display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>"
)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated flex containers to use space-between for equal visual height distribution")
