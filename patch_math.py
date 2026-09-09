import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace weakSubject
content = content.replace(
    "<div style={{ fontWeight: 700, fontSize: 15, color: 'var(--gray-800)' }}>{weakSubject}</div>",
    "<div style={{ fontWeight: 700, fontSize: 15, color: 'var(--gray-800)' }}>{weakSubject === 'Mathematics' ? 'Math' : weakSubject}</div>"
)

# Replace By Accuracy push logic
old_push_strong = "if (overallWeakSubjects[sub]?.strongWeak?.length > 0) weakest.push(sub);"
new_push_strong = "if (overallWeakSubjects[sub]?.strongWeak?.length > 0) weakest.push(sub === 'Mathematics' ? 'Math' : sub);"
content = content.replace(old_push_strong, new_push_strong)

old_push_medium = "if (overallWeakSubjects[sub]?.mediumWeak?.length > 0) weakest.push(`${sub} (Medium)`);"
new_push_medium = "if (overallWeakSubjects[sub]?.mediumWeak?.length > 0) weakest.push(`${sub === 'Mathematics' ? 'Math' : sub} (Medium)`);"
content = content.replace(old_push_medium, new_push_medium)

with open(filepath, 'w') as f:
    f.write(content)

print("Patched StudentProfileView.jsx to use Math instead of Mathematics")
