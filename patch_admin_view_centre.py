import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

target = "selectedTestKey={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : (selectedLeaderboardTestKeys[0] || selectedTestKey)} onViewStudent={setViewingStudentId} />"
replacement = "selectedTestKey={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : (selectedLeaderboardTestKeys[0] || selectedTestKey)} onViewStudent={setViewingStudentId} onViewCentre={(code) => { setFilterCenter(code); setActivePage('centre-overview'); }} />"

if target in content:
    with open(filepath, 'w') as f:
        f.write(content.replace(target, replacement))
    print("Patched AdminDashboard.jsx successfully")
else:
    print("Target not found in AdminDashboard.jsx")
