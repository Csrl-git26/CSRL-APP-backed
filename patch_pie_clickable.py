import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_cell = """                      {sorted.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={(entry.avg||0) >= overallAvg ? '#3b82f6' : '#ef4444'} />
                      ))}"""

new_cell = """                      {sorted.map((entry, index) => (
                        <Cell 
                          key={`cell-${index}`} 
                          fill={(entry.avg||0) >= overallAvg ? '#3b82f6' : '#ef4444'} 
                          style={{ cursor: onViewCentre ? 'pointer' : 'default', outline: 'none' }}
                          onClick={() => onViewCentre && onViewCentre(entry.code)}
                        />
                      ))}"""

if old_cell in content:
    content = content.replace(old_cell, new_cell)
else:
    print("old_cell not found")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched InsightsDashboard.jsx successfully")
