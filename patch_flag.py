import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace 'import { BarChart2 } from 'lucide-react';' with 'import { BarChart2, Flag } from 'lucide-react';'
if "import { BarChart2 } from 'lucide-react';" in content:
    content = content.replace("import { BarChart2 } from 'lucide-react';", "import { BarChart2, Flag } from 'lucide-react';")

with open(filepath, 'w') as f:
    f.write(content)
print("Added Flag import to CentreLeaderboard.jsx")
