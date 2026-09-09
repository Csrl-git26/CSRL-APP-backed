import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginTop: 6 }}>
              <span style={{ fontSize: 13, color: 'var(--gray-500)' }}>{selectedSubject === 'Qualification' ? 'Sorted descending by qualification rate' : 'Sorted descending by average score'}</span>
              
              {totalAppeared > 0 && (
                <div style={{ display: 'flex', gap: 10, alignItems: 'center', marginLeft: 10 }}>
                  <span style={{ fontSize: 14, color: 'var(--gray-600)', fontWeight: 700 }}>Overall CSRL Qualification:</span>
                  <span style={{ fontSize: 16, background: 'var(--gray-100)', padding: '4px 12px', borderRadius: 20, color: 'var(--gray-700)', fontWeight: 700 }}>
                    <strong style={{ color: 'var(--gray-900)' }}>{totalAppeared}</strong> Appeared
                  </span>
                  {qualPct < 80 ? (
                    <span style={{ fontSize: 16, background: '#fee2e2', color: '#991b1b', padding: '4px 12px', borderRadius: 20, fontWeight: 800, display: 'flex', alignItems: 'center', gap: 6 }}>
                      <Flag size={14} color="#cc0000" fill="#cc0000" style={{ flexShrink: 0 }} /> ATTENTION - 
                      <strong style={{ color: '#7f1d1d' }}>{totalQualified}</strong> Qualified ({qualPct}%)
                    </span>
                  ) : (
                    <span style={{ fontSize: 16, background: '#fae8ff', color: '#86198f', padding: '4px 12px', borderRadius: 20, fontWeight: 800 }}>
                      <strong style={{ color: '#701a75' }}>{totalQualified}</strong> Qualified ({qualPct}%)
                    </span>
                  )}
                </div>
              )}
            </div>"""

if old_block in content:
    with open(filepath, 'w') as f:
        f.write(content.replace(old_block, ""))
    print("Patched AdminDashboard.jsx successfully")
else:
    print("old_block not found")
