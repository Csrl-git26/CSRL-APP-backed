import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Define the block to remove
block_to_remove = """      {/* ── Centre Health + Student Dist + Category ── */}
      <div style={{ display:'grid', gridTemplateColumns:'1fr', gap:16 }}>

        {/* Centre Health */}
        <div style={{ background:'#fff', borderRadius:14, padding:'18px 20px',
          boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0' }}>
          <SectionTitle Icon={Flag} color="#1a4fa0">Centre Health</SectionTitle>
          <div style={{ display:'flex', gap:10, marginBottom:14 }}>
            <div style={{ flex:1, textAlign:'center', padding:'10px 6px', background:'#f0fdf4',
              borderRadius:10, border:'1px solid #bbf7d0' }}>
              <div style={{ fontSize:22, fontWeight:900, color:'#16a34a' }}>{healthyCentres.length}</div>
              <div style={{ fontSize:11, color:'#16a34a', fontWeight:600 }}>On Track ✅</div>
            </div>
            <div style={{ flex:1, textAlign:'center', padding:'10px 6px', background:'#fef2f2',
              borderRadius:10, border:'1px solid #fecaca' }}>
              <div style={{ fontSize:22, fontWeight:900, color:'#dc2626' }}>{redFlagCentres.length}</div>
              <div style={{ fontSize:11, color:'#dc2626', fontWeight:600 }}>Attention 🚨</div>
            </div>
          </div>
          {redFlagCentres.slice(0,5).map((c,i) => (
            <div key={c.code} style={{ display:'flex', justifyContent:'space-between', alignItems:'center',
              padding:'5px 8px', borderRadius:7, marginBottom:4, background:'#fef9f9', border:'1px solid #fee2e2' }}>
              <div style={{ display:'flex', alignItems:'center', gap:6 }}>
                <div style={{ width:6, height:6, borderRadius:'50%', background:'#dc2626', flexShrink:0 }}/>
                <span style={{ fontSize:13, fontWeight:700, color:'#1e293b' }}>{c.code}</span>
              </div>
              <div style={{ display:'flex', gap:6 }}>
                <span style={{ fontSize:11, background:'#ffe4e6', color:'#dc2626',
                  padding:'2px 7px', borderRadius:20, fontWeight:700 }}>Avg:{Math.round(c.avg)}</span>
                {c.qualRate !== undefined && (
                  <span style={{ fontSize:11, background:'#fef3c7', color:'#92400e',
                    padding:'2px 7px', borderRadius:20, fontWeight:700 }}>{Math.round(c.qualRate)}%</span>
                )}
              </div>
            </div>
          ))}
          {redFlagCentres.length > 5 && (
            <div style={{ fontSize:11, color:'#94a3b8', textAlign:'center', marginTop:6 }}>
              +{redFlagCentres.length - 5} more centres need attention
            </div>
          )}
        </div>



        {/* Category + Top States */}

      </div>"""

if block_to_remove in content:
    content = content.replace(block_to_remove, "")
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched InsightsDashboard.jsx to remove Centre Health block")
else:
    print("WARNING: Could not find block to replace in InsightsDashboard.jsx")
