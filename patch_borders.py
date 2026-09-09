import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Remove border from RankRow container
old_rankrow = """      style={{ display:'flex', alignItems:'center', gap:10, padding:'8px 10px',
      borderRadius:8, background: rank % 2 === 0 ? '#f8fafc' : '#fff',
      marginBottom:4, border:'1px solid #f1f5f9', cursor: onClick ? 'pointer' : 'default', transition: 'all 0.15s ease' }}"""
new_rankrow = """      style={{ display:'flex', alignItems:'center', gap:10, padding:'8px 10px',
      borderRadius:8, background: rank % 2 === 0 ? '#f8fafc' : '#fff',
      marginBottom:4, border:'none', cursor: onClick ? 'pointer' : 'default', transition: 'all 0.15s ease' }}"""

# Remove border from avatar
old_avatar = """      <div style={{ width:36, height:36, borderRadius:'50%', background:bg,
        color:fg, fontWeight:800, fontSize:13, display:'flex', alignItems:'center',
        justifyContent:'center', flexShrink:0, border:'2px solid rgba(0,0,0,0.07)' }}>"""
new_avatar = """      <div style={{ width:36, height:36, borderRadius:'50%', background:bg,
        color:fg, fontWeight:800, fontSize:13, display:'flex', alignItems:'center',
        justifyContent:'center', flexShrink:0, border:'none' }}>"""

if old_rankrow in content:
    content = content.replace(old_rankrow, new_rankrow)
else:
    print("old_rankrow not found")

if old_avatar in content:
    content = content.replace(old_avatar, new_avatar)
else:
    print("old_avatar not found")

with open(filepath, 'w') as f:
    f.write(content)

print("Borders removed successfully")
