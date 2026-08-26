import sys

filepath = '/Users/surya/Desktop/CSRL-APP-backed/server.js'
with open(filepath, 'r') as f:
    content = f.read()

old_global = """  const global = await loadApplicationData();
  let result = rankCentresByTest(global.profiles, global.tests, testKey, global.testColumns);
  
  const baseTestKeys = testKey.split(',').map(k => k.split('_')[0]).join(',');
  const insights = computeTestInsights(global.profiles, global.tests, baseTestKeys, global.testColumns);"""

new_global = """  const global = await loadApplicationData();
  
  let resolvedTestKey = testKey;
  if (testKey === 'ALL_FMT') {
    const fmtKeys = Array.from(new Set(global.testColumns.filter(k => k.startsWith('FMT')).map(k => k.split('_')[0])));
    resolvedTestKey = fmtKeys.join(',');
  }

  let result = rankCentresByTest(global.profiles, global.tests, resolvedTestKey, global.testColumns);
  
  const baseTestKeys = resolvedTestKey.split(',').map(k => k.split('_')[0]).join(',');
  const insights = computeTestInsights(global.profiles, global.tests, baseTestKeys, global.testColumns, { isAllFMT: testKey === 'ALL_FMT' });"""

if old_global in content:
    content = content.replace(old_global, new_global)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched global-insights successfully!")
else:
    print("Failed to find old block in server.js")
