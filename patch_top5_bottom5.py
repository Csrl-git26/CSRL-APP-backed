import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace the title and mapping logic
old_title = '<SectionTitle Icon={Star} color="#f59e0b">⭐ Top 10 Centres by Average Score</SectionTitle>'
new_title = '<SectionTitle Icon={Star} color="#f59e0b">⭐ Top 5 and Bottom 5 Centres</SectionTitle>'
content = content.replace(old_title, new_title)

# The logic block replacement
old_logic = """          <div style={{ display:'grid', gridTemplateColumns:'repeat(5,1fr)', gap:10 }}>
            {[...centreBoard].sort((a,b) => (b.avg||0)-(a.avg||0)).slice(0,10).map((c,i) => {
              const isAlert = c.avg < 100 || (c.qualRate??0) < 80;
              const medals = {0:'🥇',1:'🥈',2:'🥉'};
              return (
                <div key={c.code} style={{ padding:'12px 10px', borderRadius:10, textAlign:'center',
                  background: isAlert ? '#fef2f2' : '#f8fafc',
                  border: isAlert ? '1px solid #fecaca' : '1px solid #e2e8f0',
                  cursor: onViewCentre ? 'pointer' : 'default' }}
                  onClick={() => onViewCentre && onViewCentre(c.code)}>
                  <div style={{ fontSize:18 }}>{medals[i]||`#${i+1}`}</div>
                  <div style={{ fontWeight:800, fontSize:13, color:'#1e293b', marginTop:2 }}>{c.code}</div>
                  <div style={{ fontSize:20, fontWeight:900, color: isAlert?'#dc2626':'#1a4fa0', marginTop:2 }}>
                    {Math.round(c.avg)}
                  </div>
                  <div style={{ fontSize:10, color:'#94a3b8', marginTop:2 }}>Avg Score</div>
                  {c.qualRate !== undefined && (
                    <div style={{ marginTop:4, fontSize:11, fontWeight:700,
                      color: c.qualRate < 80 ? '#dc2626' : '#16a34a' }}>
                      {Math.round(c.qualRate)}% Qual.
                    </div>
                  )}
                </div>
              );
            })}"""

new_logic = """          <div style={{ display:'grid', gridTemplateColumns:'repeat(5,1fr)', gap:10 }}>
            {(() => {
              const sorted = [...centreBoard].sort((a,b) => (b.avg||0)-(a.avg||0));
              let displayCentres = [];
              if (sorted.length <= 10) {
                displayCentres = sorted.map((c,i) => ({...c, rank: i+1}));
              } else {
                displayCentres = [
                  ...sorted.slice(0,5).map((c,i) => ({...c, rank: i+1})),
                  ...sorted.slice(-5).map((c,i) => ({...c, rank: sorted.length - 5 + i + 1}))
                ];
              }
              return displayCentres.map((c) => {
                const isAlert = c.avg < 100 || (c.qualRate??0) < 80;
                const medals = {1:'🥇',2:'🥈',3:'🥉'};
                const rankDisplay = medals[c.rank] || `#${c.rank}`;
                return (
                  <div key={c.code} style={{ padding:'8px 6px', borderRadius:8, textAlign:'center',
                    background: isAlert ? '#fef2f2' : '#f8fafc',
                    border: isAlert ? '1px solid #fecaca' : '1px solid #e2e8f0',
                    cursor: onViewCentre ? 'pointer' : 'default' }}
                    onClick={() => onViewCentre && onViewCentre(c.code)}>
                    <div style={{ fontSize:14 }}>{rankDisplay}</div>
                    <div style={{ fontWeight:800, fontSize:12, color:'#1e293b', marginTop:2 }}>{c.code}</div>
                    <div style={{ fontSize:16, fontWeight:900, color: isAlert?'#dc2626':'#1a4fa0', marginTop:2 }}>
                      {Math.round(c.avg)}
                    </div>
                    {c.qualRate !== undefined && (
                      <div style={{ marginTop:2, fontSize:10, fontWeight:700,
                        color: c.qualRate < 80 ? '#dc2626' : '#16a34a' }}>
                        {Math.round(c.qualRate)}% Qual.
                      </div>
                    )}
                  </div>
                );
              });
            })()}"""

if old_logic in content:
    with open(filepath, 'w') as f:
        f.write(content.replace(old_logic, new_logic))
    print("Patched InsightsDashboard.jsx logic successfully")
else:
    print("old_logic not found")
