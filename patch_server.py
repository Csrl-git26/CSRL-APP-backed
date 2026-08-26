import sys

filepath = '/Users/surya/Desktop/CSRL-APP-backed/server.js'
with open(filepath, 'r') as f:
    content = f.read()

old_global_insights = """  const { testKey } = req.query;
  const baseTestKeys = testKey.split(',').map(k => k.split('_')[0]).join(',');
  const insights = computeTestInsights(global.profiles, global.tests, baseTestKeys, global.testColumns);"""

new_global_insights = """  const { testKey } = req.query;
  let baseTestKeys = testKey.split(',').map(k => k.split('_')[0]).join(',');
  if (testKey === 'ALL_FMT') {
    const fmtKeys = Array.from(new Set(Object.keys(global.testColumns).filter(k => k.startsWith('FMT')).map(k => k.split('_')[0])));
    baseTestKeys = fmtKeys.join(',');
  }
  const insights = computeTestInsights(global.profiles, global.tests, baseTestKeys, global.testColumns, { isAllFMT: testKey === 'ALL_FMT' });"""

if old_global_insights in content:
    content = content.replace(old_global_insights, new_global_insights)

old_test_insights = """  const global = await loadApplicationData();
  const result = computeTestInsights(global.profiles, global.tests, testKey, global.testColumns, {
    rollKey: rollKey || undefined,
  });"""

new_test_insights = """  const global = await loadApplicationData();
  let resolvedTestKey = testKey;
  if (testKey === 'ALL_FMT') {
    const fmtKeys = Array.from(new Set(Object.keys(global.testColumns).filter(k => k.startsWith('FMT')).map(k => k.split('_')[0])));
    resolvedTestKey = fmtKeys.join(',');
  }
  const result = computeTestInsights(global.profiles, global.tests, resolvedTestKey, global.testColumns, {
    rollKey: rollKey || undefined,
    isAllFMT: testKey === 'ALL_FMT'
  });"""

if old_test_insights in content:
    content = content.replace(old_test_insights, new_test_insights)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched server.js")
