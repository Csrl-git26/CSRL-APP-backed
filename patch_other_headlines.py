import re

files = [
    '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx',
    '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
]

new_style = "display: 'flex', alignItems: 'center', gap: 6, fontSize: 14, fontWeight: 800, color: '#2563eb', letterSpacing: '-0.3px', borderBottom: '2px solid #2563eb20', paddingBottom: 4, margin: '0 0 10px 0'"

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()
        
    # Replace Centre Rankings style
    content = content.replace(
        "<div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 18, fontWeight: 800, color: 'var(--gray-800)' }}>\n                  <Trophy",
        f"<div style={{{{ {new_style} }}}}>\n                  <Trophy"
    )
    content = content.replace(
        "<div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 18, fontWeight: 800, color: 'var(--gray-800)' }}>\n            <Trophy",
        f"<div style={{{{ {new_style} }}}}>\n            <Trophy"
    )

    # Replace Centre Performance Trend style
    content = content.replace(
        "<h2 style={{ fontSize: 16, fontWeight: 700, color: 'var(--csrl-blue)' }}>Centre Performance Trend</h2>",
        f"<h2 style={{{{ {new_style} }}}}>Centre Performance Trend</h2>"
    )
    
    with open(filepath, 'w') as f:
        f.write(content)

print("Updated headline styles in AdminDashboard.jsx and CentreDashboard.jsx to match InsightsDashboard's SectionTitle.")
