filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_return = """  return (
    <div 
      onClick={onClick}
      style={{ display:'flex', alignItems:'center', gap:10, padding:'2px 4px',
      borderRadius:8, background: rank % 2 === 0 ? '#f8fafc' : '#fff',
      marginBottom:2, border:'none', cursor: onClick ? 'pointer' : 'default', transition: 'all 0.15s ease' }}
      onMouseEnter={(e) => { if(onClick) { e.currentTarget.style.transform = 'translateY(-1px)'; e.currentTarget.style.boxShadow = '0 2px 4px rgba(0,0,0,0.05)'; } }}
      onMouseLeave={(e) => { if(onClick) { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = 'none'; } }}
    >
      <div style={{ width:16, textAlign:'center', fontSize:10, fontWeight:800, flexShrink:0,
        color: rank <= 3 ? '#f59e0b' : '#94a3b8' }}>{medals[rank] || `${rank}`}</div>
      <div style={{ flex:1, minWidth:0, display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 6 }}>
        <div style={{ fontSize:10, fontWeight:700, color:'#1e293b', whiteSpace:'nowrap' }}>{name}</div>
        <div style={{ fontSize:8, color:'#64748b', fontWeight:600 }}>{center}</div>
        {subjectScores.length > 0 && (
          <div style={{ fontSize: 8, color: '#64748b', display: 'flex', gap: 4, alignItems: 'center' }}>
            {subjectScores.map((sc, i) => (
              <span key={i} style={{ background: '#f1f5f9', padding: '1px 3px', borderRadius: 2, fontWeight: 600, border: '1px solid #e2e8f0' }}>{sc}</span>
            ))}
          </div>
        )}
      </div>
      <div style={{ background:fg+'20', color:fg, fontWeight:800,
        fontSize:10, padding:'2px 6px', borderRadius:20, flexShrink:0 }}>{score}</div>
    </div>
  );"""

new_return = """  return (
    <div 
      onClick={onClick}
      style={{ display:'flex', alignItems:'center', gap:12, padding:'7px 10px',
      borderRadius:10, background: rank % 2 === 0 ? '#f8fafc' : '#fff',
      marginBottom:4, border:'1px solid transparent', cursor: onClick ? 'pointer' : 'default', transition: 'all 0.15s ease' }}
      onMouseEnter={(e) => { if(onClick) { e.currentTarget.style.transform = 'translateY(-1px)'; e.currentTarget.style.boxShadow = '0 2px 6px rgba(37,99,235,0.08)'; e.currentTarget.style.borderColor = '#e2e8f0'; } }}
      onMouseLeave={(e) => { if(onClick) { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = 'none'; e.currentTarget.style.borderColor = 'transparent'; } }}
    >
      <div style={{ width:22, height:22, display:'flex', alignItems:'center', justifyContent:'center', fontSize:13, fontWeight:800, flexShrink:0,
        color: rank <= 3 ? '#f59e0b' : '#94a3b8' }}>{medals[rank] || rank}</div>
      <div style={{ flex:1, minWidth:0, display:'flex', flexDirection:'column', gap:3 }}>
        <div style={{ display:'flex', alignItems:'baseline', gap:8 }}>
          <div style={{ fontSize:12, fontWeight:700, color:'#1e293b', whiteSpace:'nowrap', overflow:'hidden', textOverflow:'ellipsis' }}>{name}</div>
          <div style={{ fontSize:10, color:'#94a3b8', fontWeight:600, flexShrink:0 }}>{center}</div>
        </div>
        {subjectScores.length > 0 && (
          <div style={{ display:'flex', gap:5, alignItems:'center', flexWrap:'wrap' }}>
            {subjectScores.map((sc, i) => (
              <span key={i} style={{ background:'#eef2ff', color:'#4f46e5', padding:'1px 6px', borderRadius:4, fontSize:10, fontWeight:600, letterSpacing:'-0.2px' }}>{sc}</span>
            ))}
          </div>
        )}
      </div>
      <div style={{ background:'#2563eb15', color:'#2563eb', fontWeight:800,
        fontSize:13, padding:'3px 10px', borderRadius:20, flexShrink:0, letterSpacing:'-0.3px' }}>{score}</div>
    </div>
  );"""

content = content.replace(old_return, new_return)

# Also increase the container padding slightly for breathing room
content = content.replace(
    "background:'#fff', borderRadius:14, padding:'6px 8px',\n          boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e8f0fc'",
    "background:'#fff', borderRadius:14, padding:'10px 12px',\n          boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e8f0fc'"
)

with open(filepath, 'w') as f:
    f.write(content)

print("Cleaned up RankRow layout with better spacing, two-line structure, and breathing room.")
