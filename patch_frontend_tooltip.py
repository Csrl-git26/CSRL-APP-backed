import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_tooltip_line = "<p style={{ margin: '2px 0', color: 'var(--gray-700)', fontWeight: 600 }}>Top Score: {data.top}</p>"
new_tooltip_lines = """<p style={{ margin: '2px 0', color: 'var(--gray-700)', fontWeight: 600 }}>Highest Individual Score: {data.top}</p>
        {data.bottom !== undefined && <p style={{ margin: '2px 0', color: 'var(--gray-700)', fontWeight: 600 }}>Lowest Individual Score: {data.bottom}</p>}"""

if old_tooltip_line in content:
    content = content.replace(old_tooltip_line, new_tooltip_lines)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched frontend tooltip")
else:
    print("Could not find the target string in CentreLeaderboard.jsx")
