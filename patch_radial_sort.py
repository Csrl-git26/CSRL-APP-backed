import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Remove the .reverse() on the bottom 5 slice so that when radialData does .reverse(), it ends up sorted ascending
content = content.replace(
    "const top5Qual = showBottom5Qual ? sortedByQual.slice(-5).reverse() : sortedByQual.slice(0, 5);",
    "const top5Qual = showBottom5Qual ? sortedByQual.slice(-5) : sortedByQual.slice(0, 5);"
)

with open(filepath, 'w') as f:
    f.write(content)

print("Fixed the sorting order for bottom 5 qualification rates.")
