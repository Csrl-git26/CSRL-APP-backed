import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_kpi = """function KpiCard({ icon: Icon, value, label, sub, bg, color }) {
  return (
    <div style={{ background:bg, borderRadius:12, padding:'16px 18px', display:'flex',
      alignItems:'flex-start', gap:14, boxShadow:'0 1px 4px rgba(0,0,0,0.07)', flex:1, minWidth:0 }}>
      <div style={{ width:44, height:44, borderRadius:10, background:color+'22',
        display:'flex', alignItems:'center', justifyContent:'center', flexShrink:0 }}>
        <Icon size={20} color={color}/>
      </div>
      <div style={{ minWidth:0 }}>
        <div style={{ fontSize:26, fontWeight:900, color, lineHeight:1.1 }}>{value}</div>
        <div style={{ fontSize:12, color:'#475569', fontWeight:600, marginTop:2 }}>{label}</div>
        {sub && <div style={{ fontSize:11, color:'#94a3b8', marginTop:2 }}>{sub}</div>}
      </div>
    </div>
  );
}"""

new_kpi = """function KpiCard({ icon: Icon, value, label, sub, bg, color }) {
  return (
    <div style={{ background:bg, borderRadius:10, padding:'10px 14px', display:'flex',
      alignItems:'center', gap:12, boxShadow:'0 1px 4px rgba(0,0,0,0.07)', flex:1, minWidth:0 }}>
      <div style={{ width:34, height:34, borderRadius:8, background:color+'22',
        display:'flex', alignItems:'center', justifyContent:'center', flexShrink:0 }}>
        <Icon size={18} color={color}/>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', flex: 1, minWidth: 0 }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 6 }}>
          <div style={{ fontSize:18, fontWeight:900, color, lineHeight:1.1 }}>{value}</div>
          <div style={{ fontSize:11, fontWeight:700, color:'#475569', whiteSpace:'nowrap', overflow:'hidden', textOverflow:'ellipsis' }}>{label}</div>
        </div>
        {sub && <div style={{ fontSize:10, color:'#94a3b8', marginTop:1, whiteSpace:'nowrap', overflow:'hidden', textOverflow:'ellipsis' }}>{sub}</div>}
      </div>
    </div>
  );
}"""

if old_kpi in content:
    content = content.replace(old_kpi, new_kpi)
else:
    print("old_kpi not found")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched InsightsDashboard.jsx successfully")
