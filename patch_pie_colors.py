import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace green with blue
content = content.replace("#10b981", "#3b82f6")

# Increase container height
old_height_220 = "minHeight: 220"
new_height_260 = "minHeight: 280"
content = content.replace(old_height_220, new_height_260)

old_resp_height = "height={220}"
new_resp_height = "height={280}"
content = content.replace(old_resp_height, new_resp_height)

# Increase pie radii
old_radii = """                      innerRadius={35} 
                      outerRadius={60}"""
new_radii = """                      innerRadius={55} 
                      outerRadius={85}"""
content = content.replace(old_radii, new_radii)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched InsightsDashboard.jsx successfully")
