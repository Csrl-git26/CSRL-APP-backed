import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace legendPayload calculation
old_legend = """              const legendPayload = [...radialData].reverse().map(item => ({
                value: item.name,
                type: 'square',
                color: item.fill
              }));"""

new_legend = """              const legendPayload = top5Qual.map((c, i) => ({
                value: c.code,
                type: 'square',
                color: colors[i % colors.length]
              }));"""

content = content.replace(old_legend, new_legend)

with open(filepath, 'w') as f:
    f.write(content)

print("Fixed legend order by mapping directly from top5Qual.")
