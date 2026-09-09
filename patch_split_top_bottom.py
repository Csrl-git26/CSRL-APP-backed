import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """      {centreBoard.length > 0 && (
        <div style={{ background:'#fff', borderRadius:14, padding:'18px 20px',
          boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0' }}>
          <SectionTitle Icon={Star} color="#f59e0b">⭐ Top 5 and Bottom 5 Centres</SectionTitle>
          <div style={{ display:'grid', gridTemplateColumns:'repeat(5,1fr)', gap:10 }}>
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
            })()}
          </div>"""

new_block = """      {centreBoard.length > 0 && (
        <div style={{ background:'#fff', borderRadius:14, padding:'18px 20px',
          boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0' }}>
          
          {(() => {
            const sorted = [...centreBoard].sort((a,b) => (b.avg||0)-(a.avg||0));
            const topCentres = sorted.slice(0,5).map((c,i) => ({...c, rank: i+1}));
            const bottomCentres = sorted.length > 5 ? sorted.slice(-5).map((c,i) => ({...c, rank: sorted.length - 5 + i + 1})) : [];
            
            const renderCard = (c) => {
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
            };

            return (
              <>
                <SectionTitle Icon={Star} color="#f59e0b">⭐ Top 5 Centres by Average Score</SectionTitle>
                <div style={{ display:'grid', gridTemplateColumns:'repeat(5,1fr)', gap:10, marginBottom: bottomCentres.length > 0 ? 20 : 0 }}>
                  {topCentres.map(renderCard)}
                </div>
                
                {bottomCentres.length > 0 && (
                  <>
                    <SectionTitle Icon={TrendingDown} color="#dc2626">📉 Bottom 5 Centres</SectionTitle>
                    <div style={{ display:'grid', gridTemplateColumns:'repeat(5,1fr)', gap:10 }}>
                      {bottomCentres.map(renderCard)}
                    </div>
                  </>
                )}
              </>
            );
          })()}"""

if old_block in content:
    with open(filepath, 'w') as f:
        f.write(content.replace(old_block, new_block))
    print("Patched InsightsDashboard.jsx successfully")
else:
    print("old_block not found")
