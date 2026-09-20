import os

admin_dash = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(admin_dash, 'r') as f:
    content = f.read()

# Fix fetchOverview
content = content.replace("fetchOverview(null, null, stream)", "fetchOverview(null, null, globalStream)")
content = content.replace("}, [refreshTrigger, stream]);", "}, [refreshTrigger, globalStream]);")

# Fix fetchRankings
content = content.replace("fetchRankings(null, { testKey: combinedKey, limit: 15, order: 'desc', stream })", "fetchRankings(null, { testKey: combinedKey, limit: 15, order: 'desc', stream: globalStream })")
content = content.replace("fetchRankings(null, { testKey: combinedKey, limit: 15, order: 'asc', stream })", "fetchRankings(null, { testKey: combinedKey, limit: 15, order: 'asc', stream: globalStream })")
content = content.replace("}, [selectedTestKey, selectedSubject, refreshTrigger, stream]);", "}, [selectedTestKey, selectedSubject, refreshTrigger, globalStream]);")

with open(admin_dash, 'w') as f:
    f.write(content)

print("Fixed stream -> globalStream in AdminDashboard.jsx")
