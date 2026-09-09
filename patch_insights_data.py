import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Add new state for leaderboard specific top/bottom ranked
if 'const [leaderboardTopRanked' not in content:
    content = content.replace(
        "const [topRanked,       setTopRanked]       = useState([]);",
        "const [topRanked,       setTopRanked]       = useState([]);\n  const [leaderboardTopRanked, setLeaderboardTopRanked] = useState([]);\n  const [leaderboardBottomRanked, setLeaderboardBottomRanked] = useState([]);"
    )

# 2. Modify the Leaderboard effect to also fetch top/bottom for the selected keys
old_effect = """    fetchCentreLeaderboard(null, combinedKey)
      .then(board => setCentreBoard(Array.isArray(board) ? board : []))
      .catch(() => setCentreBoard([]));
  }, [selectedLeaderboardTestKeys, selectedSubject, refreshTrigger]);"""

new_effect = """    fetchCentreLeaderboard(null, combinedKey)
      .then(board => setCentreBoard(Array.isArray(board) ? board : []))
      .catch(() => setCentreBoard([]));
      
    Promise.all([
      fetchRankings(null, { testKey: combinedKey, limit: 15, order: 'desc' }).catch(() => ({ ranked: [] })),
      fetchRankings(null, { testKey: combinedKey, limit: 15, order: 'asc'  }).catch(() => ({ ranked: [] })),
    ]).then(([top, bottom]) => {
      setLeaderboardTopRanked(top.ranked || []);
      setLeaderboardBottomRanked(bottom.ranked || []);
    });
  }, [selectedLeaderboardTestKeys, selectedSubject, refreshTrigger]);"""

content = content.replace(old_effect, new_effect)

# 3. Update the InsightsDashboard render to use the new state and the right label
old_insights = "<InsightsDashboard data={data} overview={overview} topRanked={topRanked} bottomRanked={bottomRanked} centreBoard={centreBoard} selectedTestKey={selectedTestKey} />"
new_insights = "<InsightsDashboard data={data} overview={overview} topRanked={leaderboardTopRanked} bottomRanked={leaderboardBottomRanked} centreBoard={centreBoard} selectedTestKey={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : (selectedLeaderboardTestKeys[0] || selectedTestKey)} />"

content = content.replace(old_insights, new_insights)

with open(filepath, 'w') as f:
    f.write(content)

print("Patched AdminDashboard.jsx to use leaderboard selection for insights.")
