import sys
import re

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # In Top30Section and Bottom30Section, we want to replace the `<td><strong...>{m.marks}</strong></td>` line.
    # Wait, they might have slight variations.
    pattern = r'(<td><strong[^>]*>\{m\.marks\}</strong></td>)'
    
    # We will inject the extra columns just before the pattern
    replacement = r'{allTestOptions.filter(o => String(o).startsWith(\'FMT\') && String(o) !== \'ALL_FMT\' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: \'var(--gray-400)\', fontSize: 11, textAlign: \'center\' }}>{m.fmtRanks?.[t] || \'-\'}</td>)}\n                \1'
    
    content = re.sub(pattern, replacement, content)
    
    # Let's also fix Bottom30Section's thead if it wasn't fixed by the previous script
    # The previous script might not have targeted Bottom30Section!
    # Bottom30Section thead:
    pattern_thead = r'(\{\s*allSubjects\.map\(\(s\)\s*=>\s*\{[^}]+\}\)\s*\})\s*<th>Total</th>'
    replacement_thead = r'\1\n            {allTestOptions.filter(o => String(o).startsWith(\'FMT\') && String(o) !== \'ALL_FMT\' && String(o) !== selectedTestKey).map(t => <th key={t} style={{fontSize: 10}} title={t + \' Rank\'}>{t.replace(\'FMT\',\'\')} Rk</th>)}\n            <th>Total</th>'
    
    content = re.sub(pattern_thead, replacement_thead, content)

    # Let's fix the colSpan in the "No data" row
    content = re.sub(r'colSpan=\{allSubjects\.length \+ 5\}', r'colSpan={allSubjects.length + 5 + allTestOptions.filter(o => String(o).startsWith(\'FMT\') && String(o) !== \'ALL_FMT\' && String(o) !== selectedTestKey).length}', content)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx')
patch_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx')
