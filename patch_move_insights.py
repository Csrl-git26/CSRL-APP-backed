import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Extract InsightsDashboard string
insights_str = """      <div style={{ marginTop: 24 }}>
        <InsightsDashboard data={data} overview={overview} topRanked={leaderboardTopRanked} bottomRanked={leaderboardBottomRanked} centreBoard={centreBoard} selectedTestKey={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : (selectedLeaderboardTestKeys[0] || selectedTestKey)} onViewStudent={setViewingStudentId} />
      </div>"""

# Remove InsightsDashboard from current location
content = content.replace(insights_str, "")

# Add it to the top of the InsightsSection
top_target = """    return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div className="card" style={{ padding: '16px 20px', marginBottom: 0, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 12 }}>"""

replacement = """    return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div>
        <InsightsDashboard data={data} overview={overview} topRanked={leaderboardTopRanked} bottomRanked={leaderboardBottomRanked} centreBoard={centreBoard} selectedTestKey={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : (selectedLeaderboardTestKeys[0] || selectedTestKey)} onViewStudent={setViewingStudentId} />
      </div>
      <div className="card" style={{ padding: '16px 20px', marginBottom: 0, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 12 }}>"""

content = content.replace(top_target, replacement)

with open(filepath, 'w') as f:
    f.write(content)

print("Patched AdminDashboard.jsx to move InsightsDashboard to the top (Corrected)")
