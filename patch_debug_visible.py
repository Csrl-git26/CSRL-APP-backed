import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestInsightsPanel.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_td = """                    return (
                      <td key={s} style={{ color: val === '—' ? 'var(--gray-200)' : 'inherit' }} title={r.rawScores ? Object.keys(r.rawScores).join(', ') : 'no rawScores'}>
                        {val === '—' ? (r.rawScores ? 'NoMatch' : 'NoRaw') : val}
                      </td>
                    );"""

new_td = """                    return (
                      <td key={s} style={{ color: val === '—' ? 'var(--gray-200)' : 'inherit', fontSize: '10px' }} title={r.rawScores ? Object.keys(r.rawScores).join(', ') : 'no rawScores'}>
                        {val === '—' ? (r.rawScores ? Object.keys(r.rawScores).filter(k => k.toLowerCase().includes(s.toLowerCase())).join('|') || 'NoMatch' : 'NoRaw') : val}
                      </td>
                    );"""

if old_td in content:
    content = content.replace(old_td, new_td)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched debug visible")
else:
    print("Could not find the target block")
