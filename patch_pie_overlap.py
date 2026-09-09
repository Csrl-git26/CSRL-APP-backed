import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """                      label={({ cx, cy, midAngle, outerRadius, name }) => {
                        const RADIAN = Math.PI / 180;
                        const radius = outerRadius + 12;
                        const x = cx + radius * Math.cos(-midAngle * RADIAN);
                        const y = cy + radius * Math.sin(-midAngle * RADIAN);
                        return (
                          <text x={x} y={y} fill="#64748b" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" fontSize={10}>
                            {name}
                          </text>
                        );
                      }}"""

new_block = """                      label={({ cx, cy, midAngle, outerRadius, name, index }) => {
                        const RADIAN = Math.PI / 180;
                        // Alternate radius to prevent overlapping
                        const radius = outerRadius + 12 + (index % 2 === 0 ? 0 : 14);
                        const x = cx + radius * Math.cos(-midAngle * RADIAN);
                        const y = cy + radius * Math.sin(-midAngle * RADIAN);
                        return (
                          <text x={x} y={y} fill="#64748b" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" fontSize={9}>
                            {name}
                          </text>
                        );
                      }}"""

if old_block in content:
    content = content.replace(old_block, new_block)
else:
    print("old_block not found")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched InsightsDashboard.jsx successfully")
