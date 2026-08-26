import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/Login.jsx'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("label: 'CSRL Admin'", "label: 'CSRL Management'")
content = content.replace("placeholder=\"CSRL Admin username\"", "placeholder=\"CSRL Management username\"")

with open(filepath, 'w') as f:
    f.write(content)

print("Patched Login.jsx")
