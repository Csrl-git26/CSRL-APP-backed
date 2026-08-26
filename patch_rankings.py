import sys

filepath = '/Users/surya/Desktop/CSRL-APP-backed/server.js'
with open(filepath, 'r') as f:
    content = f.read()

old_rankings = """  const source = centerCode ? await loadCenterApplicationData(centerCode) : await loadApplicationData();
  let ranked = rankStudentsByTest(source.profiles, source.tests, testKey);
  const absent = absentCount(source.profiles, source.tests, testKey);"""

new_rankings = """  const source = centerCode ? await loadCenterApplicationData(centerCode) : await loadApplicationData();
  
  let resolvedTestKey = testKey;
  if (testKey === 'ALL_FMT') {
    const fmtKeys = Array.from(new Set(source.testColumns.filter(k => k.startsWith('FMT')).map(k => k.split('_')[0])));
    resolvedTestKey = fmtKeys.join(',');
  }

  let ranked = rankStudentsByTest(source.profiles, source.tests, resolvedTestKey);
  const absent = absentCount(source.profiles, source.tests, resolvedTestKey);"""

if old_rankings in content:
    content = content.replace(old_rankings, new_rankings)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched rankings successfully!")
else:
    print("Failed to find old block in server.js")
