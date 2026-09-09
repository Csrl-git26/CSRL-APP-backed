import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Update Tooltip to use a labelFormatter that adds 1 to the index, or just hide the index and format nicely.
# Actually, the user says "NUMBERING SHOUD BE STARTVFROM 1 NOT 0"
old_tooltip = """                    <Tooltip 
                      cursor={{ fill: 'transparent' }} 
                      contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', fontSize: 12, fontWeight: 600 }} 
                      formatter={(val, name, props) => [`${val}%`, props?.payload?.name || 'Qual Rate']}
                    />"""

new_tooltip = """                    <Tooltip 
                      cursor={{ fill: 'transparent' }} 
                      contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', fontSize: 12, fontWeight: 600 }} 
                      labelFormatter={(label) => `Rank ${Number(label) + 1}`}
                      formatter={(val, name, props) => [`${val}%`, props?.payload?.name || 'Qual Rate']}
                    />"""

content = content.replace(old_tooltip, new_tooltip)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated Tooltip to display 1-based indexing for the rank label.")
