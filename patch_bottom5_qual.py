import sys
filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace line 976
old_text = '<SectionTitle Icon={PieChartIcon} color="#2563eb">BOTTOM 5 CENTRE - QUAL</SectionTitle>'
new_text = "<SectionTitle Icon={PieChartIcon} color=\"#2563eb\">{stream === 'NEET' ? 'BOTTOM 5 CENTRE - MBBS %' : 'BOTTOM 5 CENTRE - QUAL %'}</SectionTitle>"
content = content.replace(old_text, new_text)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched InsightsDashboard.jsx text for BOTTOM 5 CENTRE")
