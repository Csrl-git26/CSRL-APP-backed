import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# RankRow shrinking
content = content.replace("padding:'4px 8px'", "padding:'2px 4px'")
content = content.replace("width:24, textAlign:'center', fontSize:14", "width:16, textAlign:'center', fontSize:10")
content = content.replace("fontSize:13, fontWeight:700, color:'#1e293b'", "fontSize:10, fontWeight:700, color:'#1e293b'")
content = content.replace("fontSize:11, color:'#64748b', fontWeight:600", "fontSize:8, color:'#64748b', fontWeight:600")
content = content.replace("fontSize: 11, color: '#64748b', display: 'flex'", "fontSize: 8, color: '#64748b', display: 'flex'")
content = content.replace("padding: '2px 6px', borderRadius: 4", "padding: '1px 3px', borderRadius: 2")
content = content.replace("fontSize:13, padding:'3px 10px'", "fontSize:10, padding:'2px 6px'")

# renderCard shrinking
content = content.replace("padding:'6px 4px'", "padding:'3px 2px'")
content = content.replace("<div style={{ fontSize:14 }}>{rankDisplay}</div>", "<div style={{ fontSize:10 }}>{rankDisplay}</div>")
content = content.replace("fontWeight:800, fontSize:12, color:'#1e293b', marginTop:2", "fontWeight:800, fontSize:9, color:'#1e293b', marginTop:1")
content = content.replace("fontSize:16, fontWeight:900, color: isAlert?'#dc2626':'#1a4fa0', marginTop:2", "fontSize:12, fontWeight:900, color: isAlert?'#dc2626':'#1a4fa0', marginTop:1")
content = content.replace("marginTop:2, fontSize:10, fontWeight:700", "marginTop:1, fontSize:8, fontWeight:700")

# grid gap
content = content.replace("gridTemplateColumns:'repeat(5,1fr)', gap:6", "gridTemplateColumns:'repeat(5,1fr)', gap:3")
content = content.replace("marginBottom: bottomCentres.length > 0 ? 12 : 0", "marginBottom: bottomCentres.length > 0 ? 6 : 0")

with open(filepath, 'w') as f:
    f.write(content)

print("Scaled down text and box sizes by ~50%")
