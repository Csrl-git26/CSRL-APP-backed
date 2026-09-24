import os
filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad_str = "const parts = [physics, chemistry, math, botany, zoology, biology].filter((v) => v !== null);"
good_str = "const parts = [physics, chemistry, botany, zoology, biology].filter((v) => v !== null);"
if bad_str in content:
    content = content.replace(bad_str, good_str)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Fixed StudentDashboard.jsx crash!")
else:
    print("Could not find bad string in StudentDashboard.jsx")
