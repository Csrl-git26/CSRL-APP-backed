import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace value={totalCentres} label="Active Centres" 
# with value={centreBoard.length} label="Centres Appeared"
content = content.replace(
    'value={totalCentres} label="Active Centres"',
    'value={centreBoard.length} label="Centres Appeared"'
)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated KPI card to show centreBoard.length instead of totalCentres")
