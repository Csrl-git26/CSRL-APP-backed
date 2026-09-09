import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_pie_start = """                    <Pie 
                      data={sorted} 
                      dataKey="avg" 
                      nameKey="code" 
                      cx="50%" 
                      cy="50%" 
                      innerRadius={65} 
                      outerRadius={90} 
                      paddingAngle={1}"""

new_pie_start = """                    <Pie 
                      data={sorted.map(c => ({...c, equalValue: 1}))} 
                      dataKey="equalValue" 
                      nameKey="code" 
                      cx="50%" 
                      cy="50%" 
                      innerRadius={65} 
                      outerRadius={90} 
                      paddingAngle={1}"""

if old_pie_start in content:
    content = content.replace(old_pie_start, new_pie_start)
else:
    print("old_pie_start not found")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched InsightsDashboard.jsx successfully")
