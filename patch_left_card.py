import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_left = """<div style={{ display: 'flex', flexDirection: 'column', minWidth: 0 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 10 }}>"""
new_left = """<div className="card" style={{ display: 'flex', flexDirection: 'column', minWidth: 0, marginTop: 0, height: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 10 }}>"""

if old_left in content:
    content = content.replace(old_left, new_left)

with open(filepath, 'w') as f:
    f.write(content)
print("Added card class to left column")
