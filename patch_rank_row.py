import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """      <div style={{ flex:1, minWidth:0 }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 6 }}>
          <div style={{ fontSize:13, fontWeight:700, color:'#1e293b',
            overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap' }}>{name}</div>
          <div style={{ fontSize:11, color:'#64748b' }}>{center}</div>
        </div>
      </div>
      {subjectScores.length > 0 && (
        <div style={{ fontSize: 11, color: '#64748b', display: 'flex', gap: 6, alignItems: 'center', marginRight: 4 }}>
          {subjectScores.map((sc, i) => (
            <span key={i} style={{ background: '#f1f5f9', padding: '2px 6px', borderRadius: 4, fontWeight: 600 }}>{sc}</span>
          ))}
        </div>
      )}
      <div style={{ background:fg+'20', color:fg, fontWeight:800,"""


new_block = """      <div style={{ flex:1, minWidth:0, display: 'flex', flexDirection: 'column', gap: 6, justifyContent: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 6 }}>
          <div style={{ fontSize:13, fontWeight:700, color:'#1e293b',
            overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap' }}>{name}</div>
          <div style={{ fontSize:11, color:'#64748b', fontWeight:600 }}>{center}</div>
        </div>
        {subjectScores.length > 0 && (
          <div style={{ fontSize: 11, color: '#64748b', display: 'flex', gap: 4, alignItems: 'center', flexWrap: 'wrap' }}>
            {subjectScores.map((sc, i) => (
              <span key={i} style={{ background: '#f1f5f9', padding: '2px 6px', borderRadius: 4, fontWeight: 600, border: '1px solid #e2e8f0' }}>{sc}</span>
            ))}
          </div>
        )}
      </div>
      <div style={{ background:fg+'20', color:fg, fontWeight:800,"""

if old_block in content:
    content = content.replace(old_block, new_block)
else:
    print("old_block not found")

with open(filepath, 'w') as f:
    f.write(content)

print("RankRow patched successfully")
