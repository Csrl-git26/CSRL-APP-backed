import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """    return (
      <div>
        <div style={{ marginBottom: 32 }}>
          <InsightsDashboard data={data} overview={overview} topRanked={leaderboardTopRanked} bottomRanked={leaderboardBottomRanked} centreBoard={centreBoard} selectedTestKey={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : (selectedLeaderboardTestKeys[0] || selectedTestKey)} onViewStudent={setViewingStudentId} onViewCentre={(code) => { setFilterCenter(code); setActivePage('centre-overview'); }} />
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 10 }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 18, fontWeight: 800, color: 'var(--gray-800)' }}>
              <Trophy size={18} aria-hidden="true" />Centre Rankings — {selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : (selectedLeaderboardTestKeys[0] || selectedTestKey)}
            </div>

          </div>
        <div style={{ display: 'flex', gap: 16, alignItems: 'center' }}>
          
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <span style={{ fontSize: 13, color: 'var(--gray-600)' }}>Test:</span>
            <MultiSelectDropdown 
              options={allTestOptions.filter(o => o !== 'ALL_FMT')} 
              selectedOptions={selectedLeaderboardTestKeys} 
              onChange={setSelectedLeaderboardTestKeys} 
            />
          </div>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <span style={{ fontSize: 13, color: 'var(--gray-600)' }}>Sort By Subject:</span>
            <select className="input select" value={selectedSubject} onChange={(e) => setSelectedSubject(e.target.value)} style={{ width: 140, fontSize: 13 }}>
              <option value="Total">Total Average</option>
              <option value="Physics">Physics</option>
              <option value="Chemistry">Chemistry</option>
              <option value="Math">Math</option>
              <option value="Qualification">Qualification Rate</option>
            </select>
          </div>
        </div>
      </div>
      <CentreLeaderboard"""

new_block = """    return (
      <div>
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 16 }}>
          <div style={{ display: 'flex', gap: 16, alignItems: 'center' }}>
            <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
              <span style={{ fontSize: 13, color: 'var(--gray-600)' }}>Test:</span>
              <MultiSelectDropdown 
                options={allTestOptions.filter(o => o !== 'ALL_FMT')} 
                selectedOptions={selectedLeaderboardTestKeys} 
                onChange={setSelectedLeaderboardTestKeys} 
              />
            </div>
            <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
              <span style={{ fontSize: 13, color: 'var(--gray-600)' }}>Sort By Subject:</span>
              <select className="input select" value={selectedSubject} onChange={(e) => setSelectedSubject(e.target.value)} style={{ width: 140, fontSize: 13 }}>
                <option value="Total">Total Average</option>
                <option value="Physics">Physics</option>
                <option value="Chemistry">Chemistry</option>
                <option value="Math">Math</option>
                <option value="Qualification">Qualification Rate</option>
              </select>
            </div>
          </div>
        </div>

        <div style={{ marginBottom: 32 }}>
          <InsightsDashboard data={data} overview={overview} topRanked={leaderboardTopRanked} bottomRanked={leaderboardBottomRanked} centreBoard={centreBoard} selectedTestKey={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : (selectedLeaderboardTestKeys[0] || selectedTestKey)} onViewStudent={setViewingStudentId} onViewCentre={(code) => { setFilterCenter(code); setActivePage('centre-overview'); }} />
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 10 }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 18, fontWeight: 800, color: 'var(--gray-800)' }}>
              <Trophy size={18} aria-hidden="true" />Centre Rankings — {selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : (selectedLeaderboardTestKeys[0] || selectedTestKey)}
            </div>
          </div>
        </div>
      <CentreLeaderboard"""

if old_block in content:
    with open(filepath, 'w') as f:
        f.write(content.replace(old_block, new_block))
    print("Patched AdminDashboard.jsx successfully")
else:
    print("old_block not found")
