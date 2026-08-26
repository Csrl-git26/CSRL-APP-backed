import sys

filepath = '/Users/surya/Desktop/CSRL-APP-backed/server.js'
with open(filepath, 'r') as f:
    content = f.read()

old_insights = "const insights = computeTestInsights(global.profiles, global.tests, testKey, global.testColumns);"
new_insights = """const baseTestKeys = testKey.split(',').map(k => k.split('_')[0]).join(',');
  const insights = computeTestInsights(global.profiles, global.tests, baseTestKeys, global.testColumns);"""

if old_insights in content:
    content = content.replace(old_insights, new_insights)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched server.js for baseTestKeys")
else:
    print("Could not find insights call in server.js")
