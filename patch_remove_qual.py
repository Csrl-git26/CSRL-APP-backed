import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_qual = """                      {c.qualRate !== undefined && (
                        <div style={{ marginTop:0, fontSize:7, fontWeight:700,
                          color: isAlert ? '#dc2626' : '#1a4fa0' }}>
                          {Math.round(c.qualRate)}% Qual.
                        </div>
                      )}"""

content = content.replace(old_qual, "")

with open(filepath, 'w') as f:
    f.write(content)

print("Removed qualification percentage from centre cards.")
