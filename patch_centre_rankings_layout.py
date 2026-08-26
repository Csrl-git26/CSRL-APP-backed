import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_layout = """  const RankingsPair = () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div className="grid-2">
        <div className="card">
        <div className="section-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>"""

new_layout = """  const RankingsPair = () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        <div className="card">
        <div className="section-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>"""

if old_layout in content:
    content = content.replace(old_layout, new_layout)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched successfully!")
else:
    print("Could not find old_layout in CentreDashboard.jsx")
