import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_memo = """  const rankingTestColumns = useMemo(
    () => (data?.testColumns || [])
      .filter((c) => !String(c).includes('_'))
      .sort((a, b) => String(b).localeCompare(String(a), undefined, { numeric: true, sensitivity: 'base' })),
    [data]
  );"""

new_memo = """  const rankingTestColumns = useMemo(
    () => ['ALL_FMT', ...(data?.testColumns || [])
      .filter((c) => !String(c).includes('_'))
      .sort((a, b) => String(b).localeCompare(String(a), undefined, { numeric: true, sensitivity: 'base' }))],
    [data]
  );"""

if old_memo in content:
    content = content.replace(old_memo, new_memo)
    print("Patched rankingTestColumns successfully!")
else:
    print("Could not find old_memo in CentreDashboard.jsx")

old_select = """              {rankingTestColumns.map((t) => <option key={t} value={t} style={{ color: '#333' }}>{t}</option>)}"""
new_select = """              {rankingTestColumns.map((t) => <option key={t} value={t} style={{ color: '#333' }}>{t === 'ALL_FMT' ? 'All FMT Average' : t}</option>)}"""

if old_select in content:
    content = content.replace(old_select, new_select)
    print("Patched select successfully!")
else:
    print("Could not find old_select in CentreDashboard.jsx")

with open(filepath, 'w') as f:
    f.write(content)
