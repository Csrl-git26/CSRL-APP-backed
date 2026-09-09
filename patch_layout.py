import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace the main grid definition
content = content.replace(
    "<div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 2fr)', gap: 20 }}>",
    "<div style={{ display: 'grid', gridTemplateColumns: centreBoard.length > 0 ? 'repeat(3, minmax(0, 1fr))' : '1fr', gap: 20 }}>"
)

# Remove the nested grid in the Right Column
content = content.replace(
    "return (\n          <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: 20 }}>\n            {/* Left Column: Top and Bottom 5 */}",
    "return (\n          <>\n            {/* Left Column: Top and Bottom 5 */}"
)

# Remove the closing div of the nested grid
content = content.replace(
    "            </div>\n          </div>\n        );\n      })()}",
    "            </div>\n          </>\n        );\n      })()}"
)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated grid layout to 3 equal columns")
