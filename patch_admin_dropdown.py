import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Add 'ALL_FMT' to the dropdown options if it's not already there
old_allTestOptions = """  const allTestOptions = useMemo(
    () => [...new Set([...manualTestOptions, ...rankingTestColumns])]
      .sort((a, b) => String(b).localeCompare(String(a), undefined, { numeric: true, sensitivity: 'base' })),
    [manualTestOptions, rankingTestColumns]
  );"""

new_allTestOptions = """  const allTestOptions = useMemo(() => {
    const sorted = [...new Set([...manualTestOptions, ...rankingTestColumns])]
      .sort((a, b) => String(b).localeCompare(String(a), undefined, { numeric: true, sensitivity: 'base' }));
    return ['ALL_FMT', ...sorted];
  }, [manualTestOptions, rankingTestColumns]);"""

if old_allTestOptions in content:
    content = content.replace(old_allTestOptions, new_allTestOptions)

# Also need to display 'ALL_FMT' nicely in the select box
old_select = """              {allTestOptions.map((t) => <option key={t} value={t} style={{ color: '#333' }}>{t}</option>)}"""
new_select = """              {allTestOptions.map((t) => <option key={t} value={t} style={{ color: '#333' }}>{t === 'ALL_FMT' ? 'All FMT Average' : t}</option>)}"""

if old_select in content:
    content = content.replace(old_select, new_select)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched AdminDashboard")
