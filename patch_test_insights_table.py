import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestInsightsPanel.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Remove searchTerm state
content = content.replace("  const [searchTerm, setSearchTerm] = useState('');\n", "")

# 2. Update filteredRanked to remove searchTerm logic
old_filter = """  const filteredRanked = useMemo(() => {
    let list = [...rankedStudents];

    if (searchTerm) {
      const q = searchTerm.toLowerCase();
      list = list.filter(s => (s.name || '').toLowerCase().includes(q) || (s.roll || '').toLowerCase().includes(q));
    }

    list = list.filter(s => {"""
new_filter = """  const filteredRanked = useMemo(() => {
    let list = [...rankedStudents];

    list = list.filter(s => {"""
content = content.replace(old_filter, new_filter)

# 3. Fix useMemo dependencies
old_deps = "}, [rankedStudents, selectedCenter, sortOrder, rankMode, searchTerm, filterCategory, filterSponsor, filterGender]);"
new_deps = "}, [rankedStudents, selectedCenter, sortOrder, rankMode, filterCategory, filterSponsor, filterGender]);"
content = content.replace(old_deps, new_deps)

# 4. Remove Search UI
old_search_ui = """          <div style={{ position: 'relative', flex: '1 1 200px' }}>
            <Search size={13} style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: 'var(--gray-400)', pointerEvents: 'none' }} />
            <input
              className="input"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by name or roll…"
              style={{ width: '100%', paddingLeft: 30 }}
            />
          </div>"""
content = content.replace(old_search_ui, "")

# 5. Add subjects to table header
old_thead = """            <thead>
              <tr>
                <th>#</th>
                <th>Student</th>
                <th>Centre</th>
                <th>Total</th>
                <th>Actions</th>
              </tr>
            </thead>"""
new_thead = """            <thead>
              <tr>
                <th>#</th>
                <th>Student</th>
                <th>Centre</th>
                {subjects.map((s) => {
                  const abbr = s === 'Physics' ? 'P' : s === 'Chemistry' ? 'C' : (s === 'Math' || s === 'Mathematics') ? 'M' : s === 'Biology' ? 'B' : s.substring(0, 3);
                  return <th key={s} title={s}>{abbr}</th>;
                })}
                <th>Total</th>
                <th>Actions</th>
              </tr>
            </thead>"""
content = content.replace(old_thead, new_thead)

# 6. Add subjects to table body
old_tbody_row = """                  <td>{r.center}</td>
                  <td><strong style={{ color: '#1a4fa0' }}>{r.marks}</strong></td>"""
new_tbody_row = """                  <td>{r.center}</td>
                  {subjects.map((s) => {
                    let val = '—';
                    if (r.rawScores) {
                      const k1 = `${insights.testKey}_${s}`;
                      if (r.rawScores[k1] !== undefined && r.rawScores[k1] !== null && r.rawScores[k1] !== '') {
                        val = r.rawScores[k1];
                      } else if (r.rawScores[s] !== undefined && r.rawScores[s] !== null && r.rawScores[s] !== '') {
                        val = r.rawScores[s];
                      }
                    }
                    return (
                      <td key={s} style={{ color: val === '—' ? 'var(--gray-200)' : 'inherit' }}>
                        {val}
                      </td>
                    );
                  })}
                  <td><strong style={{ color: '#1a4fa0' }}>{r.marks}</strong></td>"""
content = content.replace(old_tbody_row, new_tbody_row)

old_colspan = "colSpan={5}"
new_colspan = "colSpan={5 + subjects.length}"
content = content.replace(old_colspan, new_colspan)

with open(filepath, 'w') as f:
    f.write(content)

print("Patched TestInsightsPanel table UI and filters")
