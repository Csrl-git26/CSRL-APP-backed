import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad = "alert('Export failed.');"
good = "alert('Export failed: ' + (err.message || err.toString()));"

if bad in content:
    content = content.replace(bad, good)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched alert successfully")
else:
    print("Could not find alert string")
