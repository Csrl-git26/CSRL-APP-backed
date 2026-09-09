import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace(
    "export default function InsightsDashboard({ data, overview, topRanked, bottomRanked, centreBoard, selectedTestKey, onViewStudent, onViewCentre }) {",
    "export default function InsightsDashboard({ data, overview, topRanked, bottomRanked, centreBoard, selectedTestKey, onViewStudent, onViewCentre }) {\n  const [showBottom5Qual, setShowBottom5Qual] = useState(false);"
)

# And fix the Top 5 Avg text that also failed earlier because I used single quotes instead of curly braces for the ternary string in JSX.
# Actually I need to check how I replaced it.
# Let's just fix it.
content = content.replace(
    "{showBottom5Qual ? 'Bot 5 Avg' : 'Top 5 Avg'}",
    "{showBottom5Qual ? 'Bottom 5 Avg' : 'Top 5 Avg'}"
)

with open(filepath, 'w') as f:
    f.write(content)

print("Inserted the useState hook successfully.")
