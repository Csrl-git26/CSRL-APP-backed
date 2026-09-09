import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Add previousPage state
content = content.replace(
    'const [viewingStudentId, setViewingStudentId] = useState(null);',
    "const [viewingStudentId, setViewingStudentId] = useState(null);\n  const [previousPage, setPreviousPage] = useState('leaderboard');"
)

# 2. Update handleLeaderboardCentreClick
content = content.replace(
    '''  const handleLeaderboardCentreClick = (code) => {
    setFilterCenter(code);
    setActivePage('centre-overview');
  };''',
    '''  const handleLeaderboardCentreClick = (code) => {
    setPreviousPage(activePage);
    setFilterCenter(code);
    setActivePage('centre-overview');
  };'''
)

# 3. Update InsightsDashboard onViewCentre
content = content.replace(
    "onViewCentre={(code) => { setFilterCenter(code); setActivePage('centre-overview'); }}",
    "onViewCentre={(code) => { setPreviousPage(activePage); setFilterCenter(code); setActivePage('centre-overview'); }}"
)

# 4. Update the ShieldCheck rendering
original_shield = '''        <div style={{ padding: 10, borderRadius: 10, background: 'rgba(255,255,255,.15)', flexShrink: 0 }}>
          <ShieldCheck size={24} color="#fff" aria-hidden="true" />
        </div>'''

new_shield = '''        {activePage === 'centre-overview' ? (
          <button type="button" onClick={() => setActivePage(previousPage || 'leaderboard')} className="btn btn-sm" style={{ background: 'rgba(255,255,255,.15)', color: '#fff', border: 'none', marginRight: 8, gap: 5, padding: 10, borderRadius: 10 }}>
            <ArrowLeft size={16} /> Back
          </button>
        ) : (
          <div style={{ padding: 10, borderRadius: 10, background: 'rgba(255,255,255,.15)', flexShrink: 0 }}>
            <ShieldCheck size={24} color="#fff" aria-hidden="true" />
          </div>
        )}'''

content = content.replace(original_shield, new_shield)

with open(filepath, 'w') as f:
    f.write(content)

print("Added Back button for Centre Overview in AdminDashboard.jsx.")
