import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace data.reduce with (data || []).reduce
content = content.replace(
    "const physicsAvg = Math.round(data.reduce((s, d) => s + (d.rawScores?.Physics||0), 0) / (data.length||1));",
    "const safeData = Array.isArray(data) ? data : [];\n              const physicsAvg = Math.round(safeData.reduce((s, d) => s + (d.rawScores?.Physics||0), 0) / (safeData.length||1));"
)
content = content.replace(
    "const chemAvg = Math.round(data.reduce((s, d) => s + (d.rawScores?.Chemistry||0), 0) / (data.length||1));",
    "const chemAvg = Math.round(safeData.reduce((s, d) => s + (d.rawScores?.Chemistry||0), 0) / (safeData.length||1));"
)
content = content.replace(
    "const mathAvg = Math.round(data.reduce((s, d) => s + (d.rawScores?.Math||d.rawScores?.Mathematics||0), 0) / (data.length||1));",
    "const mathAvg = Math.round(safeData.reduce((s, d) => s + (d.rawScores?.Math||d.rawScores?.Mathematics||0), 0) / (safeData.length||1));"
)

with open(filepath, 'w') as f:
    f.write(content)

print("Fixed data.reduce crash by ensuring data is an array.")
