import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad1 = "{activePage === 'leaderboard' && <LeaderboardSection />}"
good1 = "{activePage === 'leaderboard' && LeaderboardSection()}"

bad2 = "{activePage === 'overview'   && <OverviewSection />}"
good2 = "{activePage === 'overview'   && OverviewSection()}"

bad3 = "{activePage === 'students'   && <StudentsSection />}"
good3 = "{activePage === 'students'   && StudentsSection()}"

content = content.replace(bad1, good1)
content = content.replace(bad2, good2)
content = content.replace(bad3, good3)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched rendering to avoid component remounts")
