import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """      {/* Target & Analysis */}
      <div className="grid-2">
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div className="section-title">🎯 Target & Goals</div>
          <div>
            <div className="label">Target College / Branch</div>
            <div style={{ fontWeight: 700, fontSize: 15, color: 'var(--gray-800)', marginTop: 4 }}>
              {profile['FUTURE COLLEGE (TARGET)'] || 'Not specified'}
            </div>
          </div>
          <div className="divider" style={{ margin: '4px 0' }} />
          <div className="section-title" style={{ marginBottom: 6 }}>🧠 Weak Subject Analysis</div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>"""

new_block = """      {/* Target & Analysis */}
      <div className="grid-2">
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div className="section-title">🎯 Target & Goals</div>
          <div>
            <div className="label">Target College / Branch</div>
            <div style={{ fontWeight: 700, fontSize: 15, color: 'var(--gray-800)', marginTop: 4 }}>
              {profile['FUTURE COLLEGE (TARGET)'] || 'Not specified'}
            </div>
          </div>
        </div>
        
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div className="section-title" style={{ marginBottom: 6 }}>🧠 Weak Subject Analysis</div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched StudentProfileView.jsx to separate Target & Goals and Weak Subject Analysis into two side-by-side cards")
else:
    print("WARNING: Could not find block to replace")
