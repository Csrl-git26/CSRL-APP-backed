import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace the layout
old_layout = "display:'grid', gridTemplateColumns:'1fr 1fr', gap:16"
new_layout = "display:'grid', gridTemplateColumns:'1fr', gap:16"
content = content.replace(old_layout, new_layout)

# Remove the Student Distribution block
block_to_remove = """        {/* Student Distribution */}
        <div style={{ background:'#fff', borderRadius:14, padding:'18px 20px',
          boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0' }}>
          <SectionTitle Icon={Users} color="#1a4fa0">Student Distribution</SectionTitle>
          <div style={{ fontSize:11, fontWeight:700, color:'#64748b', marginBottom:8,
            textTransform:'uppercase', letterSpacing:0.5 }}>Gender</div>
          <ProgressBar value={maleCount}   max={totalStudents} color="#1a4fa0" bg="#e8f0fc" label="Male"   count={maleCount}/>
          <ProgressBar value={femaleCount} max={totalStudents} color="#db2777" bg="#fce7f3" label="Female" count={femaleCount}/>
          {(totalStudents-maleCount-femaleCount) > 0 && (
            <ProgressBar value={totalStudents-maleCount-femaleCount} max={totalStudents}
              color="#94a3b8" bg="#f1f5f9" label="Other" count={totalStudents-maleCount-femaleCount}/>
          )}
          <div style={{ fontSize:11, fontWeight:700, color:'#64748b', marginTop:14, marginBottom:8,
            textTransform:'uppercase', letterSpacing:0.5 }}>Stream</div>
          <ProgressBar value={jeeCount}  max={totalStudents} color="#1a4fa0" bg="#e8f0fc" label="JEE"  count={jeeCount}/>
          <ProgressBar value={neetCount} max={totalStudents} color="#16a34a" bg="#e6f5ed" label="NEET" count={neetCount}/>
        </div>"""

content = content.replace(block_to_remove, "")

with open(filepath, 'w') as f:
    f.write(content)

print("Removed Student Distribution section and updated grid layout.")
