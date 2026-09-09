import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Change Bottom 5 Centres to Star and Blue
content = content.replace(
    '<SectionTitle Icon={TrendingDown} color="#dc2626">Bottom 5 Centres</SectionTitle>',
    '<SectionTitle Icon={Star} color="#2563eb">Bottom 5 Centres</SectionTitle>'
)

# Also ensure the Qual % chart doesn't turn red when showing Bottom 5
content = content.replace(
    '<SectionTitle Icon={PieChartIcon} color={showBottom5Qual ? "#dc2626" : "#2563eb"}>',
    '<SectionTitle Icon={PieChartIcon} color="#2563eb">'
)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated Bottom 5 Centres to use Star icon and blue color.")
