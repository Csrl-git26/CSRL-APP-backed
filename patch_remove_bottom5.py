import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace the layout
old_layout = "display:'grid', gridTemplateColumns:'1fr 1fr', gap:16"
new_layout = "display:'grid', gridTemplateColumns:'1fr', gap:16"
content = content.replace(old_layout, new_layout)

# Remove the bottom 5 block
block_to_remove = """        <div style={{ background:'#fff', borderRadius:14, padding:'18px 20px',
          boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #fee2e2' }}>
          <SectionTitle Icon={AlertTriangle} color="#dc2626">⚠️ Needs Attention — Lowest Scores</SectionTitle>
          {bottom5.length === 0
            ? <div style={{ color:'#94a3b8', fontSize:13, padding:'20px 0', textAlign:'center' }}>No data available</div>
            : bottom5.map((s,i) => <RankRow key={s.roll||i} rank={i+1} name={s.name||s.roll||'—'}
                center={s.center||'—'} score={s.marks??s.score} idx={i}/>)
          }
        </div>"""

content = content.replace(block_to_remove, "")

with open(filepath, 'w') as f:
    f.write(content)

print("Removed bottom 5 students block.")
