import sys
filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace line 30
old_text_1 = "{isBottom5 ? 'BOTTOM 5 CENTRE - QUAL' : 'TOP 5 CENTRE - QUAL %'}"
new_text_1 = "{isBottom5 ? (stream === 'NEET' ? 'BOTTOM 5 CENTRE - MBBS' : 'BOTTOM 5 CENTRE - QUAL') : (stream === 'NEET' ? 'TOP 5 CENTRE - MBBS %' : 'TOP 5 CENTRE - QUAL %')}"
content = content.replace(old_text_1, new_text_1)

# Replace line 916
old_text_2 = '<SectionTitle Icon={PieChartIcon} color="#2563eb">TOP 5 CENTRE - QUAL %</SectionTitle>'
new_text_2 = "<SectionTitle Icon={PieChartIcon} color=\"#2563eb\">{stream === 'NEET' ? 'TOP 5 CENTRE - MBBS %' : 'TOP 5 CENTRE - QUAL %'}</SectionTitle>"
content = content.replace(old_text_2, new_text_2)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched InsightsDashboard.jsx text")
