import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_layout = """  const RankingsSection = () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div className="grid-2">
        <Top30Section />
        <Bottom30Section />
      </div>"""

new_layout = """  const RankingsSection = () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        <Top30Section />
        <Bottom30Section />
      </div>"""

if old_layout in content:
    content = content.replace(old_layout, new_layout)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched successfully!")
else:
    print("Could not find old_layout in AdminDashboard.jsx")
