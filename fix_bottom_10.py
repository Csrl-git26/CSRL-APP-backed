import sys

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Tbody Bottom10
    old_tbody_bottom = """                {allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: 'var(--gray-400)', fontSize: 11, textAlign: 'center' }}>{s.fmtRanks?.[t] || 'Absent'}</td>)}
                  <td><strong style={{ color: 'var(--red)' }}>{s.marks}</strong></td>"""
                  
    new_tbody_bottom = """                  <td><strong style={{ color: 'var(--red)' }}>{s.marks}</strong></td>
                  {allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: 'var(--gray-400)', fontSize: 11, textAlign: 'center' }}>{s.fmtRanks?.[t] || 'Absent'}</td>)}"""
                  
    if old_tbody_bottom in content:
        content = content.replace(old_tbody_bottom, new_tbody_bottom)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed {filepath}")
    else:
        print("Could not find the block in Bottom 10 section.")

fix_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx')
