import os

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad_botany = "delete normalized.Botany;\n"
bad_zoology = "        delete normalized.Zoology;\n"

if "delete normalized.Botany;" in content:
    content = content.replace("delete normalized.Botany;", "")
    content = content.replace("delete normalized.Zoology;", "")
    with open(filepath, 'w') as f:
        f.write(content)
    print("Fixed StudentDashboard.jsx by removing delete normalized.Botany/Zoology!")
else:
    print("Could not find delete statements.")
