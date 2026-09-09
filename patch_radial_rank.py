import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Update radialData mapping to include true rank
old_radial_data = """              const radialData = top5Qual.map((c, i) => ({
                name: c.code,
                value: Math.round(c.qualRate || 0),
                fill: colors[i % colors.length]
              })).reverse();"""

new_radial_data = """              const radialData = top5Qual.map((c, i) => {
                const rank = sortedByQual.findIndex(x => x.code === c.code) + 1;
                return {
                  name: c.code,
                  value: Math.round(c.qualRate || 0),
                  fill: colors[i % colors.length],
                  rank
                };
              }).reverse();"""

content = content.replace(old_radial_data, new_radial_data)

# Update Tooltip to use payload?.[0]?.payload?.rank
old_tooltip = """                    <Tooltip 
                      cursor={{ fill: 'transparent' }} 
                      contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', fontSize: 12, fontWeight: 600 }} 
                      labelFormatter={(label) => `Rank ${Number(label) + 1}`}
                      formatter={(val, name, props) => [`${val}%`, props?.payload?.name || 'Qual Rate']}
                    />"""

new_tooltip = """                    <Tooltip 
                      cursor={{ fill: 'transparent' }} 
                      contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', fontSize: 12, fontWeight: 600 }} 
                      labelFormatter={(label, payload) => `Rank ${payload?.[0]?.payload?.rank || (5 - Number(label))}`}
                      formatter={(val, name, props) => [`${val}%`, props?.payload?.name || 'Qual Rate']}
                    />"""

content = content.replace(old_tooltip, new_tooltip)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated RadialBarChart tooltip to use the true rank of the centre.")
