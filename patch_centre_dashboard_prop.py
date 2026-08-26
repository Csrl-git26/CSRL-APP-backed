import sys
filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_prop = """      <CentreLeaderboard 
        centreStats={centreBoard} 
        selTest={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : selectedLeaderboardTestKeys[0]} 
        onCentreClick={(code) => {"""
new_prop = """      <CentreLeaderboard 
        centreStats={centreBoard} 
        selectedSubject={selectedSubject}
        selTest={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : selectedLeaderboardTestKeys[0]} 
        onCentreClick={(code) => {"""

content = content.replace(old_prop, new_prop)

old_text = "Sorted descending by average score"
new_text = "{selectedSubject === 'Qualification' ? 'Sorted descending by qualification rate' : 'Sorted descending by average score'}"
content = content.replace(old_text, new_text)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched CentreDashboard.jsx")
