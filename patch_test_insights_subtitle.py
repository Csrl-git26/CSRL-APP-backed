import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestInsightsPanel.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_subtitle = "<p style={{ fontSize: 12, color: 'var(--gray-600)', marginBottom: 10 }}>Students who attempted but did not meet qualification rules.</p>"
new_subtitle = "<p style={{ fontSize: 12, color: 'var(--gray-600)', marginBottom: 10 }}>Total marks criteria: GEN >= 110 | EWS >= 90 | OBC >= 85 | SC >= 65 | ST >= 60 | PWD >= 30</p>"

if old_subtitle in content:
    content = content.replace(old_subtitle, new_subtitle)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched subtitle successfully!")
else:
    print("Could not find old_subtitle in TestInsightsPanel.jsx")
