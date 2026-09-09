import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace the layout
old_layout = "display:'grid', gridTemplateColumns:'1fr 1fr 1fr', gap:16"
new_layout = "display:'grid', gridTemplateColumns:'1fr 1fr', gap:16"
content = content.replace(old_layout, new_layout)

# Remove the Category Breakdown block
block_to_remove = """        <div style={{ background:'#fff', borderRadius:14, padding:'18px 20px',
          boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0' }}>
          <SectionTitle Icon={BookOpen} color="#7c3aed">Category Breakdown</SectionTitle>
          {catEntries.map(([cat,count],i) => {
            const colors = ['#1a4fa0','#16a34a','#b45309','#7c3aed','#0891b2','#dc2626'];
            const bgs    = ['#e8f0fc','#e6f5ed','#fff3e0','#f3f0ff','#e0f7fa','#fef2f2'];
            return <ProgressBar key={cat} value={count} max={totalStudents}
              color={colors[i%colors.length]} bg={bgs[i%bgs.length]} label={cat} count={count}/>;
          })}
          {topStates.length > 0 && <>
            <div style={{ fontSize:11, fontWeight:700, color:'#64748b', marginTop:14, marginBottom:8,
              textTransform:'uppercase', letterSpacing:0.5 }}>Top States</div>
            {topStates.map(([state,count]) => (
              <div key={state} style={{ display:'flex', justifyContent:'space-between', alignItems:'center',
                padding:'4px 0', borderBottom:'1px solid #f1f5f9' }}>
                <span style={{ fontSize:12, color:'#475569', fontWeight:600 }}>{state}</span>
                <span style={{ fontSize:12, fontWeight:800, color:'#1a4fa0',
                  background:'#e8f0fc', padding:'1px 8px', borderRadius:12 }}>{count}</span>
              </div>
            ))}
          </>}
        </div>"""

content = content.replace(block_to_remove, "")

with open(filepath, 'w') as f:
    f.write(content)

print("Removed Category Breakdown section and updated grid layout.")
