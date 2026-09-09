import re

# 1. Update PerformanceChart.jsx
perf_path = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/PerformanceChart.jsx'
with open(perf_path, 'r') as f:
    content = f.read()

# export default function PerformanceChart({ chartData, streamCfg, noCard }) {
# -> export default function PerformanceChart({ chartData, streamCfg, noCard, height = 350 }) {
content = content.replace(
    'export default function PerformanceChart({ chartData, streamCfg, noCard }) {',
    'export default function PerformanceChart({ chartData, streamCfg, noCard, height = 350 }) {'
)
content = content.replace(
    '<ResponsiveContainer width="100%" height={350}>',
    '<ResponsiveContainer width="100%" height={height}>'
)
with open(perf_path, 'w') as f:
    f.write(content)

# 2. Update CentreLeaderboard.jsx
board_path = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(board_path, 'r') as f:
    content = f.read()

content = content.replace(
    'export default function CentreLeaderboard({ centreStats = [], selTest, selectedSubject, onCentreClick }) {',
    'export default function CentreLeaderboard({ centreStats = [], selTest, selectedSubject, onCentreClick, height = 320 }) {'
)
content = content.replace(
    "<div style={{ width: '100%', height: 320, marginTop: 0 }}>",
    "<div style={{ width: '100%', height, marginTop: 0 }}>"
)
with open(board_path, 'w') as f:
    f.write(content)

# 3. Update AdminDashboard.jsx
admin_path = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(admin_path, 'r') as f:
    content = f.read()

# find <CentreLeaderboard and add height={240}
content = content.replace(
    '<CentreLeaderboard centreStats={centreBoard} selTest={selectedLeaderboardTestKeys.length > 1 ? \'Multiple Tests\' : selectedLeaderboardTestKeys[0]} onCentreClick={handleLeaderboardCentreClick} selectedSubject={selectedSubject} />',
    '<CentreLeaderboard centreStats={centreBoard} selTest={selectedLeaderboardTestKeys.length > 1 ? \'Multiple Tests\' : selectedLeaderboardTestKeys[0]} onCentreClick={handleLeaderboardCentreClick} selectedSubject={selectedSubject} height={240} />'
)

# find <PerformanceChart chartData={trendChartData} streamCfg={getStreamConfig('JEE')} noCard={true} />
# and add height={240}
content = content.replace(
    '<PerformanceChart chartData={trendChartData} streamCfg={getStreamConfig(\'JEE\')} noCard={true} />',
    '<PerformanceChart chartData={trendChartData} streamCfg={getStreamConfig(\'JEE\')} noCard={true} height={240} />'
)

with open(admin_path, 'w') as f:
    f.write(content)

print("Updated charts height in AdminDashboard")
