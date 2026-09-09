import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Remove from bottom
insights_str = """      <div style={{ marginTop: 24 }}>
        <InsightsDashboard data={data} overview={overview} topRanked={leaderboardTopRanked} bottomRanked={leaderboardBottomRanked} centreBoard={centreBoard} selectedTestKey={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : (selectedLeaderboardTestKeys[0] || selectedTestKey)} onViewStudent={setViewingStudentId} />
      </div>"""

if insights_str in content:
    content = content.replace(insights_str, "")
else:
    print("WARNING: Could not find insights_str at bottom")

# Add to top
top_target = """    return (
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 10 }}>"""

replacement = """    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
        <div>
          <InsightsDashboard data={data} overview={overview} topRanked={leaderboardTopRanked} bottomRanked={leaderboardBottomRanked} centreBoard={centreBoard} selectedTestKey={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : (selectedLeaderboardTestKeys[0] || selectedTestKey)} onViewStudent={setViewingStudentId} />
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 10 }}>"""

if top_target in content:
    content = content.replace(top_target, replacement)
    print("Patched AdminDashboard.jsx to move InsightsDashboard")
else:
    print("WARNING: Could not find top_target")

with open(filepath, 'w') as f:
    f.write(content)

