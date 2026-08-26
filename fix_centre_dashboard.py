import sys
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Fix thead (inject Total and FMT Ranks)
    # The current thead is:
    # {rankingSubjects.map((s) => { ... })}
    # <th>Total</th>
    # We want: <th>Total</th> \n {allTestOptions...}
    pattern_thead = r'(return <th key=\{s\} title=\{s\}>\{abbr\}</th>;\n\s*\})\n\s*<th>Total</th>'
    replacement_thead = r'\1\n              <th>Total</th>\n              {allTestOptions.filter(o => String(o).startsWith(\'FMT\') && String(o) !== \'ALL_FMT\' && String(o) !== selectedTestKey).map(t => <th key={t} style={{fontSize: 10}} title={t + \' Rank\'}>{t} Rank</th>)}'
    
    content = re.sub(pattern_thead, replacement_thead, content)

    # 2. Fix tbody Top10
    # Currently:
    # {allTestOptions.filter...}
    # <td><strong style={{ color: '#1a4fa0' }}>{s.marks}</strong></td>
    # We want to swap them so Total (s.marks) is before the test options.
    pattern_tbody_top = r'(\{\s*allTestOptions\.filter[^\}]+\}\)\s*\})\n\s*<td><strong style=\{\{ color: \'#1a4fa0\' \}\}>\{s\.marks\}</strong></td>'
    replacement_tbody_top = r'<td><strong style={{ color: \'#1a4fa0\' }}>{s.marks}</strong></td>\n                  \1'
    
    content = re.sub(pattern_tbody_top, replacement_tbody_top, content)

    # 3. Fix tbody Bottom10
    # Currently:
    # {allTestOptions.filter...}
    # <td><strong style={{ color: 'var(--red)' }}>{s.marks}</strong></td>
    pattern_tbody_bottom = r'(\{\s*allTestOptions\.filter[^\}]+\}\)\s*\})\n\s*<td><strong style=\{\{ color: \'var\(--red\)\' \}\}>\{s\.marks\}</strong></td>'
    replacement_tbody_bottom = r'<td><strong style={{ color: \'var(--red)\' }}>{s.marks}</strong></td>\n                  \1'
    
    content = re.sub(pattern_tbody_bottom, replacement_tbody_bottom, content)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed {filepath}")

fix_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx')
