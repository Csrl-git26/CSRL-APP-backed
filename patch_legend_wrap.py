import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """                <div style={{ display: 'flex', gap: 16, marginTop: 10, fontSize: 12, color: '#475569', justifyContent: 'center', width: '100%' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <div style={{ width: 10, height: 10, borderRadius: '50%', backgroundColor: '#10b981' }} />
                    Above Average
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <div style={{ width: 10, height: 10, borderRadius: '50%', backgroundColor: '#ef4444' }} />
                    Below Average
                  </div>
                </div>"""

new_block = """                <div style={{ display: 'flex', gap: 16, marginTop: 15, fontSize: 13, color: '#475569', justifyContent: 'center', width: '100%', flexWrap: 'wrap' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, whiteSpace: 'nowrap' }}>
                    <div style={{ width: 12, height: 12, borderRadius: '50%', backgroundColor: '#10b981', flexShrink: 0 }} />
                    <span style={{ fontWeight: 600 }}>Above Average</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, whiteSpace: 'nowrap' }}>
                    <div style={{ width: 12, height: 12, borderRadius: '50%', backgroundColor: '#ef4444', flexShrink: 0 }} />
                    <span style={{ fontWeight: 600 }}>Below Average</span>
                  </div>
                </div>"""

if old_block in content:
    content = content.replace(old_block, new_block)
else:
    print("old_block not found")

old_pie_radii = """                      innerRadius={40} 
                      outerRadius={70}"""

new_pie_radii = """                      innerRadius={35} 
                      outerRadius={60}"""

if old_pie_radii in content:
    content = content.replace(old_pie_radii, new_pie_radii)
else:
    print("old_pie_radii not found")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched InsightsDashboard.jsx successfully")
