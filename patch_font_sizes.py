import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Change bar label font size and weight
content = content.replace(
    'fontSize={15} fontWeight={900}', 
    'fontSize={12} fontWeight={500}'
)

# 2. Change XAxis tick font size and weight
content = content.replace(
    "tick={{ fontSize: 14, fill: '#1e293b', fontWeight: 'bold' }}",
    "tick={{ fontSize: 11, fill: '#1e293b', fontWeight: 500 }}"
)

with open(filepath, 'w') as f:
    f.write(content)
print("Updated font sizes and weights in CentreLeaderboard.jsx")
