import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """                      <div style={{ fontSize:8 }}>{rankDisplay}</div>
                      <div style={{ fontWeight:800, fontSize:8, color:'#1e293b', marginTop:0 }}>{c.code}</div>
                      <div style={{ fontSize:10, fontWeight:900, color: isAlert?'#dc2626':'#1a4fa0', marginTop:0 }}>
                        {Math.round(c.avg)}
                      </div>"""

new_code = """                      <div style={{ fontSize:8, display:'flex', justifyContent:'center', alignItems:'center', gap: 4 }}>
                        {rankDisplay} <span style={{ fontWeight:800, color:'#1e293b' }}>{c.code}</span>
                      </div>
                      <div style={{ fontSize:10, fontWeight:900, color: isAlert?'#dc2626':'#1a4fa0', marginTop:0 }}>
                        {Math.round(c.avg)}
                      </div>"""

content = content.replace(old_code, new_code)

with open(filepath, 'w') as f:
    f.write(content)

print("Placed rank and code inline for Top 5 Centres cards")
