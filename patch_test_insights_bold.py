import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestInsightsPanel.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_li = "<li key={code} style={{ color: 'var(--red)' }}>"
new_li = "<li key={code} style={{ color: 'var(--red)', fontWeight: 600 }}>"

if old_li in content:
    content = content.replace(old_li, new_li)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched successfully!")
else:
    print("Could not find old_li in TestInsightsPanel.jsx")
