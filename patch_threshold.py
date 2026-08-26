import re

filepath = '../CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("isRedFlag = data.avg <= 30;", "isRedFlag = data.avg <= 20;")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched threshold")
