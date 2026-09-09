import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Pattern to remove the avatar block
old_avatar_block = """      <div style={{ width:24, textAlign:'center', fontSize:14, fontWeight:800, flexShrink:0,
        color: rank <= 3 ? '#f59e0b' : '#94a3b8' }}>{medals[rank] || `#${rank}`}</div>
      <div style={{ width:36, height:36, borderRadius:'50%', background:bg,
        color:fg, fontWeight:800, fontSize:13, display:'flex', alignItems:'center',
        justifyContent:'center', flexShrink:0, border:'none' }}>
        {rank === 1 ? '🌟' : getInitials(name)}
      </div>
      <div style={{ flex:1, minWidth:0, display: 'flex', flexDirection: 'column', gap: 6, justifyContent: 'center' }}>"""

new_avatar_block = """      <div style={{ width:24, textAlign:'center', fontSize:14, fontWeight:800, flexShrink:0,
        color: rank <= 3 ? '#f59e0b' : '#94a3b8' }}>{medals[rank] || `#${rank}`}</div>
      <div style={{ flex:1, minWidth:0, display: 'flex', flexDirection: 'column', gap: 6, justifyContent: 'center' }}>"""


if old_avatar_block in content:
    content = content.replace(old_avatar_block, new_avatar_block)
    print("Avatar removed successfully")
else:
    print("old_avatar_block not found")

with open(filepath, 'w') as f:
    f.write(content)
