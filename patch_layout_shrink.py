import sys

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx', 'r') as f:
    content = f.read()

# Shrink Performance Graphs
content = content.replace("height: '150px'", "height: '100px'")
content = content.replace("height={150}", "height={100}")
content = content.replace("margin={{ top: 10, left: -25, bottom: 0, right: 10 }}", "margin={{ top: 5, left: -25, bottom: -5, right: 10 }}")

# Shrink Table
content = content.replace("fontSize: '11px'", "fontSize: '9px'")
content = content.replace("padding: '10px 8px'", "padding: '6px 6px'")
content = content.replace("padding: '12px'", "padding: '8px'")
content = content.replace("marginBottom: '12px'", "marginBottom: '8px'")
content = content.replace("marginBottom: '16px'", "marginBottom: '8px'")

# Shrink Main Header
content = content.replace("padding: '24px'", "padding: '16px'")
content = content.replace("paddingBottom: '16px'", "paddingBottom: '8px'")
content = content.replace("marginBottom: '24px'", "marginBottom: '12px'")
content = content.replace("width: '100px'", "width: '70px'")
content = content.replace("height: '100px'", "height: '70px'")

# Shrink Info Grid
content = content.replace("gap: '24px'", "gap: '12px'")

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx', 'w') as f:
    f.write(content)

print("Patched layout sizes.")
