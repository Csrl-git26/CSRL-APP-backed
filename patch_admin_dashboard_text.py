import sys
filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_text = "Sorted descending by average score"
new_text = "{selectedSubject === 'Qualification' ? 'Sorted descending by qualification rate' : 'Sorted descending by average score'}"
content = content.replace(old_text, new_text)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched AdminDashboard.jsx text")
