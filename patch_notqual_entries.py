import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """        {data.notQualBySub && Object.keys(data.notQualBySub).length > 0 && (
          <div style={{ marginTop: 8, padding: '6px 8px', background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 4 }}>
            <div style={{ fontSize: 11, fontWeight: 700, color: '#ef4444', marginBottom: 4, letterSpacing: 0.5 }}>No. of student subjectwise marks &lt;=20</div>
            {Object.entries(data.notQualBySub).map(([subj, count]) => (
              <div key={subj} style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: '#ef4444', marginBottom: 2 }}>
                <span>{subj}</span>
                <span style={{ fontWeight: 600 }}>{count}</span>
              </div>
            ))}
          </div>
        )}"""

new_block = """        {(() => {
          if (!data.notQualBySub) return null;
          const entries = Object.entries(data.notQualBySub).filter(([subj]) => {
            if (!selectedSubject || selectedSubject === 'Total' || selectedSubject === 'Qualification') return true;
            return subj === selectedSubject;
          });
          if (entries.length === 0) return null;
          
          const title = (!selectedSubject || selectedSubject === 'Total' || selectedSubject === 'Qualification')
            ? "No. of student subjectwise marks <=20"
            : `No. of student marks in ${selectedSubject} <=20`;
            
          return (
            <div style={{ marginTop: 8, padding: '6px 8px', background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 4 }}>
              <div style={{ fontSize: 11, fontWeight: 700, color: '#ef4444', marginBottom: 4, letterSpacing: 0.5 }}>{title}</div>
              {entries.map(([subj, count]) => (
                <div key={subj} style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: '#ef4444', marginBottom: 2 }}>
                  <span>{subj}</span>
                  <span style={{ fontWeight: 600 }}>{count}</span>
                </div>
              ))}
            </div>
          );
        })()}"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched CustomTooltip for subject-specific <= 20 box")
else:
    print("Could not find the target string!")

