import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace RadialBar with added label
old_radial = """                    <RadialBar 
                      minAngle={15} 
                      background={{ fill: '#f1f5f9' }} 
                      clockWise={true} 
                      dataKey="value" 
                      cornerRadius={10}
                    />"""

new_radial = """                    <RadialBar 
                      minAngle={15} 
                      background={{ fill: '#f1f5f9' }} 
                      clockWise={true} 
                      dataKey="value" 
                      cornerRadius={10}
                      label={{ position: 'insideStart', fill: '#fff', fontSize: 9, fontWeight: 700, formatter: (val) => `${val}%` }}
                    />"""

content = content.replace(old_radial, new_radial)

# Remove the two text elements
text_pattern = re.compile(r'<text.*?x="50%".*?y="50%".*?>\s*\{avgQual\}%\s*</text>', re.DOTALL)
content = text_pattern.sub('', content)

text_pattern2 = re.compile(r'<text.*?x="50%".*?y="65%".*?>\s*Top 5 Avg\s*</text>', re.DOTALL)
content = text_pattern2.sub('', content)

with open(filepath, 'w') as f:
    f.write(content)

print("Removed center text and added label to RadialBar.")
