import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace all occurrences of color="#f59e0b" in SectionTitle with color="#2563eb"
content = re.sub(r'<SectionTitle Icon=\{([^}]+)\} color="#f59e0b">', r'<SectionTitle Icon={\1} color="#2563eb">', content)

# And for the toggle logic in the middle column
content = content.replace(
    '<SectionTitle Icon={PieChartIcon} color={showBottom5Qual ? "#dc2626" : "#f59e0b"}>',
    '<SectionTitle Icon={PieChartIcon} color={showBottom5Qual ? "#dc2626" : "#2563eb"}>'
)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated headline colors to blue.")
