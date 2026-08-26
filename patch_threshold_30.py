import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_string = "isRedFlag = data.avg <= 20;"
new_string = "isRedFlag = data.avg <= 30;"

if old_string in content:
    content = content.replace(old_string, new_string)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched red flag threshold to 30")
else:
    print("Could not find the target string!")

