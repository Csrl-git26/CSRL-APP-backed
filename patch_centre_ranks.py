import sys
import re

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Thead injection
    pattern_thead = r'(\{\s*rankingSubjects\.map\(\(s\)\s*=>\s*\{[^}]+\}\)\s*\})\s*<th>Total</th>'
    replacement_thead = r'\1\n              {allTestOptions.filter(o => String(o).startsWith(\'FMT\') && String(o) !== \'ALL_FMT\' && String(o) !== selectedTestKey).map(t => <th key={t} style={{fontSize: 10}} title={t + \' Rank\'}>{t} Rank</th>)}\n              <th>Total</th>'
    
    content = re.sub(pattern_thead, replacement_thead, content)

    # Tbody injection (in CentreDashboard.jsx it might be different)
    pattern_tbody = r'(<td><strong[^>]*>\{s\.marks\}</strong></td>)'
    replacement_tbody = r'{allTestOptions.filter(o => String(o).startsWith(\'FMT\') && String(o) !== \'ALL_FMT\' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: \'var(--gray-400)\', fontSize: 11, textAlign: \'center\' }}>{s.fmtRanks?.[t] || \'-\'}</td>)}\n                  \1'
    
    content = re.sub(pattern_tbody, replacement_tbody, content)

    # No data colspan injection
    content = re.sub(r'colSpan=\{rankingSubjects\.length \+ 2\}', r'colSpan={rankingSubjects.length + 2 + allTestOptions.filter(o => String(o).startsWith(\'FMT\') && String(o) !== \'ALL_FMT\' && String(o) !== selectedTestKey).length}', content)
    content = re.sub(r'colSpan=\{rankingSubjects\.length \+ 3\}', r'colSpan={rankingSubjects.length + 3 + allTestOptions.filter(o => String(o).startsWith(\'FMT\') && String(o) !== \'ALL_FMT\' && String(o) !== selectedTestKey).length}', content)


    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx')
