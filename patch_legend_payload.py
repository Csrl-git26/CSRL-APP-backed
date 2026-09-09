import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Create legendPayload right after radialData
old_data_decl = """              }).reverse();
              
              const avgQual = Math.round(top5Qual.reduce((s, c) => s + (c.qualRate||0), 0) / (top5Qual.length||1));"""

new_data_decl = """              }).reverse();
              
              const legendPayload = [...radialData].reverse().map(item => ({
                value: item.name,
                type: 'square',
                color: item.fill
              }));
              
              const avgQual = Math.round(top5Qual.reduce((s, c) => s + (c.qualRate||0), 0) / (top5Qual.length||1));"""

content = content.replace(old_data_decl, new_data_decl)

# Update Legend component to use payload
old_legend = """<Legend iconSize={8} layout="vertical" verticalAlign="middle" wrapperStyle={{ right: 0, fontSize: 10 }} />"""
new_legend = """<Legend iconSize={8} layout="vertical" verticalAlign="middle" wrapperStyle={{ right: 0, fontSize: 10 }} payload={legendPayload} />"""

content = content.replace(old_legend, new_legend)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated Legend to use custom payload matching the rings from outside-in.")
