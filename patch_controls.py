import re

filepath_admin = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath_admin, 'r') as f:
    content_admin = f.read()

old_admin_block = """    return (
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
        </div>"""

new_admin_block = """    const controls = (
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
    );

    return (
      <div>
        <div style={{ marginBottom: 32 }}>
          <InsightsDashboard data={data} overview={overview} topRanked={leaderboardTopRanked} bottomRanked={leaderboardBottomRanked} centreBoard={centreBoard} selectedTestKey={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : (selectedLeaderboardTestKeys[0] || selectedTestKey)} onViewStudent={setViewingStudentId} onViewCentre={(code) => { setFilterCenter(code); setActivePage('centre-overview'); }} controls={controls} />
        </div>"""

if old_admin_block in content_admin:
    content_admin = content_admin.replace(old_admin_block, new_admin_block)
else:
    print("old_admin_block not found")

with open(filepath_admin, 'w') as f:
    f.write(content_admin)


filepath_insights = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath_insights, 'r') as f:
    content_insights = f.read()

old_insights_props = """export default function InsightsDashboard({ data, overview, topRanked, bottomRanked, centreBoard, selectedTestKey, onViewStudent, onViewCentre }) {"""
new_insights_props = """export default function InsightsDashboard({ data, overview, topRanked, bottomRanked, centreBoard, selectedTestKey, onViewStudent, onViewCentre, controls }) {"""

old_insights_top5 = """      {/* ── Top 5 + Bottom 5 ── */}
      <div style={{ display:'grid', gridTemplateColumns:'1fr', gap:16 }}>
        <div style={{ background:'#fff', borderRadius:14, padding:'18px 20px',
          boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e8f0fc' }}>
          <SectionTitle Icon={Trophy} color="#f59e0b">Top 5 Students — {selectedTestKey||'Overall'}</SectionTitle>"""

new_insights_top5 = """      {/* ── Top 5 + Bottom 5 ── */}
      <div style={{ display:'grid', gridTemplateColumns:'1fr', gap:16 }}>
        <div style={{ background:'#fff', borderRadius:14, padding:'18px 20px',
          boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e8f0fc' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 10 }}>
            <SectionTitle Icon={Trophy} color="#f59e0b">Top 5 Students — {selectedTestKey||'Overall'}</SectionTitle>
            {controls && <div style={{ marginBottom: 14 }}>{controls}</div>}
          </div>"""

if old_insights_props in content_insights:
    content_insights = content_insights.replace(old_insights_props, new_insights_props)
else:
    print("old_insights_props not found")

if old_insights_top5 in content_insights:
    content_insights = content_insights.replace(old_insights_top5, new_insights_top5)
else:
    print("old_insights_top5 not found")

with open(filepath_insights, 'w') as f:
    f.write(content_insights)

print("Patched successfully")
