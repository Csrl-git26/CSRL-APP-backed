import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # AdminDashboard thead
    content = content.replace(
        "{allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <th key={t} style={{fontSize: 10}} title={t + ' Rank'}>{t} Rank</th>)}\n            <th>Total</th>",
        "<th>Total</th>\n            {allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <th key={t} style={{fontSize: 10}} title={t + ' Rank'}>{t} Rank</th>)}"
    )

    # CentreDashboard thead
    content = content.replace(
        "{allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <th key={t} style={{fontSize: 10}} title={t + ' Rank'}>{t} Rank</th>)}\n              <th>Total</th>",
        "<th>Total</th>\n              {allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <th key={t} style={{fontSize: 10}} title={t + ' Rank'}>{t} Rank</th>)}"
    )

    # AdminDashboard tbody Top30Section
    content = content.replace(
        "{allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: 'var(--gray-400)', fontSize: 11, textAlign: 'center' }}>{m.fmtRanks?.[t] || '-'}</td>)}\n                <td><strong style={{ fontSize: 13, color: '#1a4fa0' }}>{m.marks}</strong></td>",
        "<td><strong style={{ fontSize: 13, color: '#1a4fa0' }}>{m.marks}</strong></td>\n                {allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: 'var(--gray-400)', fontSize: 11, textAlign: 'center' }}>{m.fmtRanks?.[t] || '-'}</td>)}"
    )

    # AdminDashboard tbody Bottom30Section
    content = content.replace(
        "{allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: 'var(--gray-400)', fontSize: 11, textAlign: 'center' }}>{m.fmtRanks?.[t] || '-'}</td>)}\n                <td><strong style={{ fontSize: 13, color: 'var(--red)' }}>{m.marks}</strong></td>",
        "<td><strong style={{ fontSize: 13, color: 'var(--red)' }}>{m.marks}</strong></td>\n                {allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: 'var(--gray-400)', fontSize: 11, textAlign: 'center' }}>{m.fmtRanks?.[t] || '-'}</td>)}"
    )

    # CentreDashboard tbody Top30Section
    content = content.replace(
        "{allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: 'var(--gray-400)', fontSize: 11, textAlign: 'center' }}>{s.fmtRanks?.[t] || '-'}</td>)}\n                  <td><strong style={{ fontSize: 13, color: '#1a4fa0' }}>{s.marks}</strong></td>",
        "<td><strong style={{ fontSize: 13, color: '#1a4fa0' }}>{s.marks}</strong></td>\n                  {allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: 'var(--gray-400)', fontSize: 11, textAlign: 'center' }}>{s.fmtRanks?.[t] || '-'}</td>)}"
    )

    # CentreDashboard tbody Bottom30Section
    content = content.replace(
        "{allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: 'var(--gray-400)', fontSize: 11, textAlign: 'center' }}>{s.fmtRanks?.[t] || '-'}</td>)}\n                  <td><strong style={{ fontSize: 13, color: 'var(--red)' }}>{s.marks}</strong></td>",
        "<td><strong style={{ fontSize: 13, color: 'var(--red)' }}>{s.marks}</strong></td>\n                  {allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: 'var(--gray-400)', fontSize: 11, textAlign: 'center' }}>{s.fmtRanks?.[t] || '-'}</td>)}"
    )

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx')
patch_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx')
