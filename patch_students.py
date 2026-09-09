import re

# 1. Patch AdminDashboard.jsx
filepath_admin = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath_admin, 'r') as f:
    content_admin = f.read()

old_insights_call = "<InsightsDashboard data={data} overview={overview} topRanked={leaderboardTopRanked} bottomRanked={leaderboardBottomRanked} centreBoard={centreBoard} selectedTestKey={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : (selectedLeaderboardTestKeys[0] || selectedTestKey)} />"
new_insights_call = "<InsightsDashboard data={data} overview={overview} topRanked={leaderboardTopRanked} bottomRanked={leaderboardBottomRanked} centreBoard={centreBoard} selectedTestKey={selectedLeaderboardTestKeys.length > 1 ? 'Multiple Tests' : (selectedLeaderboardTestKeys[0] || selectedTestKey)} onViewStudent={setViewingStudentId} />"

if old_insights_call in content_admin:
    content_admin = content_admin.replace(old_insights_call, new_insights_call)
    with open(filepath_admin, 'w') as f:
        f.write(content_admin)
    print("Patched AdminDashboard.jsx")
else:
    print("WARNING: Could not find InsightsDashboard call in AdminDashboard.jsx")

# 2. Patch InsightsDashboard.jsx
filepath_insights = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath_insights, 'r') as f:
    content_insights = f.read()

# Replace RankRow component
old_rankrow = """function RankRow({ rank, name, center, score, idx }) {
  const [fg, bg] = AVATAR_COLORS[idx % AVATAR_COLORS.length];
  const medals = { 1:'🥇', 2:'🥈', 3:'🥉' };
  return (
    <div style={{ display:'flex', alignItems:'center', gap:10, padding:'8px 10px',
      borderRadius:8, background: rank % 2 === 0 ? '#f8fafc' : '#fff',
      marginBottom:4, border:'1px solid #f1f5f9' }}>
      <div style={{ width:24, textAlign:'center', fontSize:14, fontWeight:800, flexShrink:0,
        color: rank <= 3 ? '#f59e0b' : '#94a3b8' }}>{medals[rank] || `#${rank}`}</div>
      <div style={{ width:36, height:36, borderRadius:'50%', background:bg,
        color:fg, fontWeight:800, fontSize:13, display:'flex', alignItems:'center',
        justifyContent:'center', flexShrink:0, border:'2px solid rgba(0,0,0,0.07)' }}>
        {rank === 1 ? '🌟' : getInitials(name)}
      </div>
      <div style={{ flex:1, minWidth:0 }}>
        <div style={{ fontSize:13, fontWeight:700, color:'#1e293b',
          overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap' }}>{name}</div>
        <div style={{ fontSize:11, color:'#64748b' }}>{center}</div>
      </div>
      <div style={{ background:fg+'20', color:fg, fontWeight:800,
        fontSize:13, padding:'3px 10px', borderRadius:20, flexShrink:0 }}>{score}</div>
    </div>
  );
}"""

new_rankrow = """function RankRow({ rank, name, center, score, idx, roll, rawScores, onClick }) {
  const [fg, bg] = AVATAR_COLORS[idx % AVATAR_COLORS.length];
  const medals = { 1:'🥇', 2:'🥈', 3:'🥉' };
  
  const subjects = ['Physics', 'Chemistry', 'Math', 'Mathematics', 'Biology', 'Botany', 'Zoology'];
  const subjectScores = [];
  if (rawScores) {
    subjects.forEach(sub => {
      if (rawScores[sub] !== undefined && rawScores[sub] !== null) {
        let abbr = sub.substring(0, 3);
        if (sub === 'Mathematics') abbr = 'Mat';
        subjectScores.push(`${abbr}: ${rawScores[sub]}`);
      }
    });
  }

  return (
    <div 
      onClick={onClick}
      style={{ display:'flex', alignItems:'center', gap:10, padding:'8px 10px',
      borderRadius:8, background: rank % 2 === 0 ? '#f8fafc' : '#fff',
      marginBottom:4, border:'1px solid #f1f5f9', cursor: onClick ? 'pointer' : 'default', transition: 'all 0.15s ease' }}
      onMouseEnter={(e) => { if(onClick) { e.currentTarget.style.transform = 'translateY(-1px)'; e.currentTarget.style.boxShadow = '0 2px 4px rgba(0,0,0,0.05)'; } }}
      onMouseLeave={(e) => { if(onClick) { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = 'none'; } }}
    >
      <div style={{ width:24, textAlign:'center', fontSize:14, fontWeight:800, flexShrink:0,
        color: rank <= 3 ? '#f59e0b' : '#94a3b8' }}>{medals[rank] || `#${rank}`}</div>
      <div style={{ width:36, height:36, borderRadius:'50%', background:bg,
        color:fg, fontWeight:800, fontSize:13, display:'flex', alignItems:'center',
        justifyContent:'center', flexShrink:0, border:'2px solid rgba(0,0,0,0.07)' }}>
        {rank === 1 ? '🌟' : getInitials(name)}
      </div>
      <div style={{ flex:1, minWidth:0 }}>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: 6 }}>
          <div style={{ fontSize:13, fontWeight:700, color:'#1e293b',
            overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap' }}>{name}</div>
          <div style={{ fontSize:11, color:'#64748b' }}>{center}</div>
        </div>
        {subjectScores.length > 0 && (
          <div style={{ fontSize: 10, color: '#64748b', marginTop: 2, display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            {subjectScores.map((sc, i) => (
              <span key={i} style={{ background: '#f1f5f9', padding: '1px 5px', borderRadius: 4, fontWeight: 600 }}>{sc}</span>
            ))}
          </div>
        )}
      </div>
      <div style={{ background:fg+'20', color:fg, fontWeight:800,
        fontSize:13, padding:'3px 10px', borderRadius:20, flexShrink:0 }}>{score}</div>
    </div>
  );
}"""

if old_rankrow in content_insights:
    content_insights = content_insights.replace(old_rankrow, new_rankrow)
else:
    print("WARNING: Could not find RankRow component in InsightsDashboard.jsx")

# Replace InsightsDashboard signature
old_sig = "export default function InsightsDashboard({ data, overview, topRanked, bottomRanked, centreBoard, selectedTestKey }) {"
new_sig = "export default function InsightsDashboard({ data, overview, topRanked, bottomRanked, centreBoard, selectedTestKey, onViewStudent }) {"
if old_sig in content_insights:
    content_insights = content_insights.replace(old_sig, new_sig)
else:
    print("WARNING: Could not find InsightsDashboard signature")

# Replace top5.map
old_map = "            : top5.map((s,i) => <RankRow key={s.roll||i} rank={i+1} name={s.name||s.roll||'—'}\n                center={s.center||'—'} score={s.marks??s.score} idx={i}/>)"
new_map = "            : top5.map((s,i) => <RankRow key={s.roll||i} rank={i+1} name={s.name||s.roll||'—'}\n                center={s.center||'—'} score={s.marks??s.score} idx={i} roll={s.roll} rawScores={s.rawScores} onClick={() => onViewStudent && onViewStudent(s.roll)} />)"

if old_map in content_insights:
    content_insights = content_insights.replace(old_map, new_map)
else:
    print("WARNING: Could not find top5.map in InsightsDashboard.jsx")

with open(filepath_insights, 'w') as f:
    f.write(content_insights)

print("Patched InsightsDashboard.jsx")
