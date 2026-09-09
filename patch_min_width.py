import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Add minWidth: 0 to Left Side
old_left = """<div style={{ display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 10 }}>"""
new_left = """<div style={{ display: 'flex', flexDirection: 'column', minWidth: 0 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 10 }}>"""

# Add minWidth: 0 to Right Side
old_right = """<div className="card" style={{ marginTop: 0, height: '100%', display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>"""
new_right = """<div className="card" style={{ marginTop: 0, height: '100%', display: 'flex', flexDirection: 'column', minWidth: 0 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>"""

if old_left in content:
    content = content.replace(old_left, new_left)
if old_right in content:
    content = content.replace(old_right, new_right)

# Wait, there are TWO instances of these.
# Let's just do a global replace for these specific strings since they are identical in both places.

with open(filepath, 'w') as f:
    f.write(content)
print("Added minWidth: 0")
