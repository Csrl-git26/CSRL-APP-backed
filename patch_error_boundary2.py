import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# find all imports and move them to the top
imports = re.findall(r'^import .*?;?\n', content, re.MULTILINE)
content = re.sub(r'^import .*?;?\n', '', content, flags=re.MULTILINE)

final_content = "".join(imports) + "\n" + content

with open(filepath, 'w') as f:
    f.write(final_content)
