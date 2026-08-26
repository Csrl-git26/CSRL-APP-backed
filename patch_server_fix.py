import sys

filepath = '/Users/surya/Desktop/CSRL-APP-backed/server.js'
with open(filepath, 'r') as f:
    content = f.read()

# Fix in global-insights
old_global = "const fmtKeys = Array.from(new Set(Object.keys(global.testColumns).filter(k => k.startsWith('FMT')).map(k => k.split('_')[0])));"
new_global = "const fmtKeys = Array.from(new Set(global.testColumns.filter(k => k.startsWith('FMT')).map(k => k.split('_')[0])));"

if old_global in content:
    content = content.replace(old_global, new_global)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched server.js")
