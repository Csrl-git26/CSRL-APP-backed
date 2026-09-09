import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """<div style={{ flex: 1, minHeight: 220, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>"""
new_block = """<div style={{ flex: 1, minHeight: 220, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>"""

if old_block in content:
    content = content.replace(old_block, new_block)
else:
    print("old_block not found")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched InsightsDashboard.jsx successfully")
