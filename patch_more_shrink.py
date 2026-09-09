import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("padding:'3px 2px'", "padding:'1px 1px'")
content = content.replace("<div style={{ fontSize:10 }}>{rankDisplay}</div>", "<div style={{ fontSize:8 }}>{rankDisplay}</div>")
content = content.replace("fontWeight:800, fontSize:9, color:'#1e293b', marginTop:1", "fontWeight:800, fontSize:8, color:'#1e293b', marginTop:0")
content = content.replace("fontSize:12, fontWeight:900, color: isAlert?'#dc2626':'#1a4fa0', marginTop:1", "fontSize:10, fontWeight:900, color: isAlert?'#dc2626':'#1a4fa0', marginTop:0")
content = content.replace("marginTop:1, fontSize:8, fontWeight:700", "marginTop:0, fontSize:7, fontWeight:700")

with open(filepath, 'w') as f:
    f.write(content)

print("Shrunk Top/Bottom Centres boxes further by reducing padding and margins to 0/1px and text size down.")
