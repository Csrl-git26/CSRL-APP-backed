import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 10 }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 18, fontWeight: 800, color: 'var(--gray-800)' }}>
              <Trophy size={18} aria-hidden="true" />Centre Rankings — {selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : (selectedLeaderboardTestKeys[0] || selectedTestKey)}
            </div>
          </div>
        </div>
      <CentreLeaderboard centreStats={centreBoard} selTest={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : selectedLeaderboardTestKeys[0]} onCentreClick={handleLeaderboardCentreClick} selectedSubject={selectedSubject} />
        <div className="card" style={{ marginTop: 0 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
            <h2 style={{ fontSize: 16, fontWeight: 700, color: 'var(--csrl-blue)' }}>Centre Performance Trend</h2>
            <select
              className="input select"
              value={selectedTrendCentre}
              onChange={(e) => setSelectedTrendCentre(e.target.value)}
              style={{ width: 200, fontSize: 13 }}
            >
              {[...centreBoard].sort((a, b) => String(a.code).localeCompare(String(b.code))).map(c => (
                <option key={c.code} value={c.code}>{c.code}</option>
              ))}
            </select>
          </div>
          {trendChartLoading ? (
            <div style={{ padding: 40, textAlign: 'center', color: 'var(--gray-500)' }}>Loading trend data...</div>
          ) : trendChartData.length > 0 ? (
            <PerformanceChart chartData={trendChartData} streamCfg={getStreamConfig('JEE')} noCard={true} />
          ) : (
            <div style={{ padding: 40, textAlign: 'center', color: 'var(--gray-500)' }}>No trend data available for this centre.</div>
          )}
        </div>"""


new_code = """        <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)', gap: '20px' }}>
          {/* Left Side: Centre Rankings (Bar Chart) */}
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 10 }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 18, fontWeight: 800, color: 'var(--gray-800)' }}>
                  <Trophy size={18} aria-hidden="true" />Centre Rankings — {selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : (selectedLeaderboardTestKeys[0] || selectedTestKey)}
                </div>
              </div>
            </div>
            <div style={{ flex: 1 }}>
              <CentreLeaderboard centreStats={centreBoard} selTest={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : selectedLeaderboardTestKeys[0]} onCentreClick={handleLeaderboardCentreClick} selectedSubject={selectedSubject} />
            </div>
          </div>
          
          {/* Right Side: Centre Performance Trend (Line Chart) */}
          <div className="card" style={{ marginTop: 0, height: '100%', display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
              <h2 style={{ fontSize: 16, fontWeight: 700, color: 'var(--csrl-blue)' }}>Centre Performance Trend</h2>
              <select
                className="input select"
                value={selectedTrendCentre}
                onChange={(e) => setSelectedTrendCentre(e.target.value)}
                style={{ width: 200, fontSize: 13 }}
              >
                {[...centreBoard].sort((a, b) => String(a.code).localeCompare(String(b.code))).map(c => (
                  <option key={c.code} value={c.code}>{c.code}</option>
                ))}
              </select>
            </div>
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
              {trendChartLoading ? (
                <div style={{ padding: 40, textAlign: 'center', color: 'var(--gray-500)' }}>Loading trend data...</div>
              ) : trendChartData.length > 0 ? (
                <PerformanceChart chartData={trendChartData} streamCfg={getStreamConfig('JEE')} noCard={true} />
              ) : (
                <div style={{ padding: 40, textAlign: 'center', color: 'var(--gray-500)' }}>No trend data available for this centre.</div>
              )}
            </div>
          </div>
        </div>"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("Code patched successfully!")
else:
    print("Old code not found!")

with open(filepath, 'w') as f:
    f.write(content)

