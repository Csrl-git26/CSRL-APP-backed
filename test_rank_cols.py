import sys
import re

def patch_admin_dashboard(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find the top of Top30Section
    extra_cols_logic = "    const extraRankCols = allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey);"

    # Replace the th in Top30Section
    content = content.replace(
        "            {allSubjects.map((s) => {\n              const abbr = s === 'Physics' ? 'P' : s === 'Chemistry' ? 'C' : (s === 'Math' || s === 'Mathematics') ? 'M' : s === 'Biology' ? 'B' : s.substring(0, 3);\n              return <th key={s} title={s}>{abbr}</th>;\n            })}\n            <th>Total</th>",
        "            {allSubjects.map((s) => {\n              const abbr = s === 'Physics' ? 'P' : s === 'Chemistry' ? 'C' : (s === 'Math' || s === 'Mathematics') ? 'M' : s === 'Biology' ? 'B' : s.substring(0, 3);\n              return <th key={s} title={s}>{abbr}</th>;\n            })}\n            {allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <th key={t} style={{fontSize: 10}} title={t + ' Rank'}>{t.replace('FMT','')} Rk</th>)}\n            <th>Total</th>"
    )

    # Replace the td in Top30Section
    content = content.replace(
        "                {allSubjects.map(s => (\n                  <td key={s} style={{ color: 'var(--gray-700)' }}>{flatM.subjects[s] ?? '-'}</td>\n                ))}\n                <td style={{ fontWeight: 800, color: 'var(--csrl-blue)', fontSize: 14 }}>{m.marks}</td>",
        "                {allSubjects.map(s => (\n                  <td key={s} style={{ color: 'var(--gray-700)' }}>{flatM.subjects[s] ?? '-'}</td>\n                ))}\n                {allTestOptions.filter(o => String(o).startsWith('FMT') && String(o) !== 'ALL_FMT' && String(o) !== selectedTestKey).map(t => <td key={t} style={{ color: 'var(--gray-400)', fontSize: 11, textAlign: 'center' }}>{m.fmtRanks?.[t] || '-'}</td>)}\n                <td style={{ fontWeight: 800, color: 'var(--csrl-blue)', fontSize: 14 }}>{m.marks}</td>"
    )

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_admin_dashboard('/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx')
patch_admin_dashboard('/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx')
