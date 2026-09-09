import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace(
    "const [fg, bg] = AVATAR_COLORS[idx % AVATAR_COLORS.length];",
    "const [fg, bg] = AVATAR_COLORS[0];"
)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated RankRow to always use the blue color")
