import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestInsightsPanel.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_span = """                  <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--gray-400)', marginLeft: 6 }}>
                    ({insights.bestScorePercentStudent.total} / {insights.bestScorePercentStudent.maxTotal ?? '—'})
                  </span>"""

if old_span in content:
    content = content.replace(old_span, "")
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched successfully!")
else:
    print("Could not find old_span in TestInsightsPanel.jsx")
