import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Add "Qualification Rate" option
old_options = """              <option value="Total">Total Average</option>
              <option value="Physics">Physics</option>
              <option value="Chemistry">Chemistry</option>
              <option value="Math">Math</option>
            </select>"""
new_options = """              <option value="Total">Total Average</option>
              <option value="Physics">Physics</option>
              <option value="Chemistry">Chemistry</option>
              <option value="Math">Math</option>
              <option value="Qualification">Qualification Rate</option>
            </select>"""
content = content.replace(old_options, new_options)

# 2. Fix combinedKey logic
old_fetch = """    const combinedKey = selectedSubject === 'Total' 
       ? baseKeys 
       : selectedLeaderboardTestKeys.map(k => `${k}_${selectedSubject}`).join(',');"""
new_fetch = """    const combinedKey = (selectedSubject === 'Total' || selectedSubject === 'Qualification')
       ? baseKeys 
       : selectedLeaderboardTestKeys.map(k => `${k}_${selectedSubject}`).join(',');"""
content = content.replace(old_fetch, new_fetch)

# 3. Pass selectedSubject to CentreLeaderboard
old_leaderboard = "      <CentreLeaderboard centreStats={centreBoard} selTest={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : selectedLeaderboardTestKeys[0]} onCentreClick={handleLeaderboardCentreClick} />"
new_leaderboard = "      <CentreLeaderboard centreStats={centreBoard} selTest={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : selectedLeaderboardTestKeys[0]} onCentreClick={handleLeaderboardCentreClick} selectedSubject={selectedSubject} />"
content = content.replace(old_leaderboard, new_leaderboard)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched AdminDashboard.jsx")
