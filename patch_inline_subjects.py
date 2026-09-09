import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """      <div style={{ flex:1, minWidth:0, display: 'flex', flexDirection: 'column', gap: 2, justifyContent: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 6 }}>
          <div style={{ fontSize:10, fontWeight:700, color:'#1e293b',
            overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap' }}>{name}</div>
          <div style={{ fontSize:8, color:'#64748b', fontWeight:600 }}>{center}</div>
        </div>
        {subjectScores.length > 0 && (
          <div style={{ fontSize: 8, color: '#64748b', display: 'flex', gap: 4, alignItems: 'center', flexWrap: 'wrap' }}>
            {subjectScores.map((sc, i) => (
              <span key={i} style={{ background: '#f1f5f9', padding: '1px 3px', borderRadius: 2, fontWeight: 600, border: '1px solid #e2e8f0' }}>{sc}</span>
            ))}
          </div>
        )}
      </div>"""

new_code = """      <div style={{ flex:1, minWidth:0, display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 6 }}>
        <div style={{ fontSize:10, fontWeight:700, color:'#1e293b', whiteSpace:'nowrap' }}>{name}</div>
        <div style={{ fontSize:8, color:'#64748b', fontWeight:600 }}>{center}</div>
        {subjectScores.length > 0 && (
          <div style={{ fontSize: 8, color: '#64748b', display: 'flex', gap: 4, alignItems: 'center' }}>
            {subjectScores.map((sc, i) => (
              <span key={i} style={{ background: '#f1f5f9', padding: '1px 3px', borderRadius: 2, fontWeight: 600, border: '1px solid #e2e8f0' }}>{sc}</span>
            ))}
          </div>
        )}
      </div>"""

content = content.replace(old_code, new_code)

with open(filepath, 'w') as f:
    f.write(content)

print("Placed subject scores inline with name and centre to save vertical space.")
