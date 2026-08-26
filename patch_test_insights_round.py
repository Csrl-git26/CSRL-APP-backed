import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestInsightsPanel.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_percent = """                <div style={{ fontSize: 22, fontWeight: 800, color: '#1a6e3b' }}>
                  {insights.bestScorePercentStudent.scorePercent}%

                </div>"""

new_percent = """                <div style={{ fontSize: 22, fontWeight: 800, color: '#1a6e3b' }}>
                  {insights.bestScorePercentStudent.scorePercent}%
                  <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--gray-400)', marginLeft: 6 }}>
                    ({Math.round(insights.bestScorePercentStudent.total)} / {insights.bestScorePercentStudent.maxTotal ?? '—'})
                  </span>
                </div>"""

if old_percent in content:
    content = content.replace(old_percent, new_percent)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched successfully!")
else:
    print("Could not find old_percent in TestInsightsPanel.jsx")
