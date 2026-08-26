import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_weakest = "<p style={{ margin: '8px 0 0 0', color: '#ef4444', fontWeight: 700 }}>Weakest: {data.weakSubject}</p>"
new_weakest = "{(!selectedSubject || selectedSubject === 'Total') && <p style={{ margin: '8px 0 0 0', color: '#ef4444', fontWeight: 700 }}>Weakest: {data.weakSubject}</p>}"

if old_weakest in content:
    content = content.replace(old_weakest, new_weakest)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched Weakest subject in CentreLeaderboard.jsx")
else:
    print("Could not find the target string!")

