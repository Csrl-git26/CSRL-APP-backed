import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestInsightsPanel.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_title = "Top student (total and score %)"
new_title = "Top student"

if old_title in content:
    content = content.replace(old_title, new_title)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched successfully!")
else:
    print("Could not find old_title in TestInsightsPanel.jsx")
