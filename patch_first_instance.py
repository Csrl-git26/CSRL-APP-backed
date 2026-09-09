import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """        <div className="grid-2">
          <div className="card">
            <div className="section-title">
              <Trophy size={15} style={{ marginRight: 6 }} aria-hidden="true" />
              Top Centres — {selectedTestKey}
            </div>
            <CentreLeaderboard centreStats={centreBoard} selTest={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : selectedLeaderboardTestKeys[0]} onCentreClick={handleLeaderboardCentreClick} selectedSubject={selectedSubject} />
        <div className="card" style={{ marginTop: 0 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
            <h2 style={{ fontSize: 16, fontWeight: 700, color: 'var(--csrl-blue)' }}>Centre Performance Trend</h2>"""

new_code = """        <div className="grid-2">
          <div className="card" style={{ display: 'flex', flexDirection: 'column' }}>
            <div className="section-title">
              <Trophy size={15} style={{ marginRight: 6 }} aria-hidden="true" />
              Top Centres — {selectedTestKey}
            </div>
            <div style={{ flex: 1 }}>
              <CentreLeaderboard centreStats={centreBoard} selTest={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : selectedLeaderboardTestKeys[0]} onCentreClick={handleLeaderboardCentreClick} selectedSubject={selectedSubject} />
            </div>
          </div>
          
          <div className="card" style={{ marginTop: 0, height: '100%', display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
              <h2 style={{ fontSize: 16, fontWeight: 700, color: 'var(--csrl-blue)' }}>Centre Performance Trend</h2>"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("First instance patched successfully!")
else:
    print("First instance old code not found!")

with open(filepath, 'w') as f:
    f.write(content)

