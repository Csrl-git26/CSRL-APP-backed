import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace the gap in the stacked left column
content = content.replace(
    "<div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>",
    "<div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>"
)

with open(filepath, 'w') as f:
    f.write(content)

print("Reduced the gap between stacked cards to half (10px)")
