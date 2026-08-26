import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if '<div className="card">' in line and 'All students rankwise' in lines[i+2] if i+2 < len(lines) else False:
        skip = True
    if skip and '<div className="card"' in line and 'Test Analysis Tab' in lines[i+1] if i+1 < len(lines) else False:
        skip = False
    
    if not skip:
        new_lines.append(line)

with open(filepath, 'w') as f:
    f.writelines(new_lines)
    
print("Patched CentreDashboard rankwise table")
