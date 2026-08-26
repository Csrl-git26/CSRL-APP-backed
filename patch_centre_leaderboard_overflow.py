import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_text = """        <text x={centerX} y={topY + (isRedFlag ? 12 : 0)} fill={textColor} textAnchor="middle" fontSize={15} fontWeight={900}>
          {value}{isQualSort ? '%' : ''}
        </text>"""

new_text = """        <text x={centerX} y={topY + (isRedFlag ? 12 : 0)} fill={textColor} textAnchor="middle" fontSize={15} fontWeight={900}>
          {typeof value === 'number' ? Math.round(value) : value}{isQualSort ? '%' : ''}
        </text>"""

if old_text in content:
    content = content.replace(old_text, new_text)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched CentreLeaderboard.jsx label format")
else:
    print("Could not find the target text block")

