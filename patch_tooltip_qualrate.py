import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_qual_line = "{data.qualRate !== undefined && <p style={{ margin: '2px 0', color: data.qualRate < 80 ? '#ef4444' : 'var(--gray-700)', fontWeight: data.qualRate < 80 ? 700 : 600 }}>Qual. Rate: {Math.round(data.qualRate)}%</p>}"

new_qual_line = "{(!selectedSubject || selectedSubject === 'Total' || selectedSubject === 'Qualification') && data.qualRate !== undefined && <p style={{ margin: '2px 0', color: data.qualRate < 80 ? '#ef4444' : 'var(--gray-700)', fontWeight: data.qualRate < 80 ? 700 : 600 }}>Qual. Rate: {Math.round(data.qualRate)}%</p>}"

if old_qual_line in content:
    content = content.replace(old_qual_line, new_qual_line)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched CustomTooltip in CentreLeaderboard.jsx")
else:
    print("Could not find the target string!")

