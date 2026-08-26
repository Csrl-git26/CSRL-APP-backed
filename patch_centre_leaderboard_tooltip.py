import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_tooltip = "{data.qualRate !== undefined && <p style={{ margin: '2px 0', color: data.qualRate < 50 ? '#ef4444' : 'var(--gray-700)', fontWeight: data.qualRate < 50 ? 700 : 600 }}>Qual. Rate: {data.qualRate}%</p>}"

new_tooltip = "{data.qualRate !== undefined && <p style={{ margin: '2px 0', color: data.qualRate < 50 ? '#ef4444' : 'var(--gray-700)', fontWeight: data.qualRate < 50 ? 700 : 600 }}>Qual. Rate: {Math.round(data.qualRate)}%</p>}"

if old_tooltip in content:
    content = content.replace(old_tooltip, new_tooltip)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched CentreLeaderboard.jsx tooltip format")
else:
    print("Could not find the target text block for tooltip")

