import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestInsightsPanel.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_td = """                  {subjects.map((s) => {
                    let val = '—';
                    if (r.rawScores) {
                      const k1 = `${insights.testKey}_${s}`;
                      if (r.rawScores[k1] !== undefined && r.rawScores[k1] !== null && r.rawScores[k1] !== '') {
                        val = r.rawScores[k1];
                      } else if (r.rawScores[s] !== undefined && r.rawScores[s] !== null && r.rawScores[s] !== '') {
                        val = r.rawScores[s];
                      }
                    }
                    return (
                      <td key={s} style={{ color: val === '—' ? 'var(--gray-200)' : 'inherit' }}>
                        {val}
                      </td>
                    );
                  })}"""

new_td = """                  {subjects.map((s) => {
                    let val = '—';
                    if (r.rawScores) {
                      const k1 = `${insights.testKey}_${s}`;
                      if (r.rawScores[k1] !== undefined && r.rawScores[k1] !== null && r.rawScores[k1] !== '') {
                        val = r.rawScores[k1];
                      } else if (r.rawScores[s] !== undefined && r.rawScores[s] !== null && r.rawScores[s] !== '') {
                        val = r.rawScores[s];
                      } else {
                        const fallbackKey = Object.keys(r.rawScores).find(k => k.toLowerCase().endsWith(s.toLowerCase()) || k.toLowerCase().includes(`_${s.toLowerCase()}`));
                        if (fallbackKey && r.rawScores[fallbackKey] !== undefined && r.rawScores[fallbackKey] !== null && r.rawScores[fallbackKey] !== '') {
                          val = r.rawScores[fallbackKey];
                        }
                      }
                    }
                    return (
                      <td key={s} style={{ color: val === '—' ? 'var(--gray-200)' : 'inherit' }}>
                        {val}
                      </td>
                    );
                  })}"""

if old_td in content:
    content = content.replace(old_td, new_td)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched TestInsightsPanel with robust subject extraction")
else:
    print("Could not find the target block")
