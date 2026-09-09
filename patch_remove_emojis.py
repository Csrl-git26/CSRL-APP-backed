import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("🏆 Top 5 Students", "Top 5 Students")
content = content.replace("⭐ Top 5 Centres by Average Score", "Top 5 Centres by Average Score")
content = content.replace("📉 Bottom 5 Centres", "Bottom 5 Centres")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched InsightsDashboard.jsx successfully")
