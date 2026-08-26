import sys

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Thead
    old_thead = """                return <th key={s} title={s}>{abbr}</th>;
              })}
              <th>Total</th>"""
              
    new_thead = """                return <th key={s} title={s}>{abbr}</th>;
              })}
              <th>Total</th>
              {allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <th key={t} style={{fontSize: 10}} title={t + ' Rank'}>{t} Rank</th>)}"""
              
    content = content.replace(old_thead, new_thead)

    # 2. Tbody Top10
    old_tbody_top = """                  {allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: 'var(--gray-400)', fontSize: 11, textAlign: 'center' }}>{s.fmtRanks?.[t] || 'Absent'}</td>)}
                  <td><strong style={{ color: '#1a4fa0' }}>{s.marks}</strong></td>"""
                  
    new_tbody_top = """                  <td><strong style={{ color: '#1a4fa0' }}>{s.marks}</strong></td>
                  {allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: 'var(--gray-400)', fontSize: 11, textAlign: 'center' }}>{s.fmtRanks?.[t] || 'Absent'}</td>)}"""
                  
    content = content.replace(old_tbody_top, new_tbody_top)
    
    # 3. Tbody Bottom10
    old_tbody_bottom = """                  {allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: 'var(--gray-400)', fontSize: 11, textAlign: 'center' }}>{s.fmtRanks?.[t] || 'Absent'}</td>)}
                  <td><strong style={{ color: 'var(--red)' }}>{s.marks}</strong></td>"""
                  
    new_tbody_bottom = """                  <td><strong style={{ color: 'var(--red)' }}>{s.marks}</strong></td>
                  {allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: 'var(--gray-400)', fontSize: 11, textAlign: 'center' }}>{s.fmtRanks?.[t] || 'Absent'}</td>)}"""
                  
    content = content.replace(old_tbody_bottom, new_tbody_bottom)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed {filepath}")

fix_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx')
