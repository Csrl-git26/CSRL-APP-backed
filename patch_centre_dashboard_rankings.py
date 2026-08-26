import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Define filteredRanked below allRanked
old_all_ranked = """  const allRanked = useMemo(() => {
    if (!data || !selectedTestKey) return [];
    return rankStudentsByTest(data.profiles, data.tests, selectedTestKey);
  }, [data, selectedTestKey]);"""

new_all_ranked = """  const allRanked = useMemo(() => {
    if (!data || !selectedTestKey) return [];
    return rankStudentsByTest(data.profiles, data.tests, selectedTestKey);
  }, [data, selectedTestKey]);

  const filteredRanked = useMemo(() => {
    let list = [...allRanked];
    if (searchTerm) {
      const lower = searchTerm.toLowerCase();
      list = list.filter(s => s.name.toLowerCase().includes(lower) || s.roll.toLowerCase().includes(lower));
    }
    list = list.filter(s => {
      const p = profileByRoll.get(s.roll);
      if (!p) return true;
      if (filterSponsor !== 'ALL' && p.SPONSOR !== filterSponsor) return false;
      if (filterStream !== 'ALL' && p.STREAM !== filterStream && s.stream !== filterStream) return false;
      if (filterCategory !== 'ALL' && p.CATEGORY !== filterCategory) return false;
      if (filterGender !== 'ALL' && p.GENDER !== filterGender) return false;
      if (filterState !== 'ALL' && p['STATE (from where completing class 12th)'] !== filterState) return false;
      return true;
    });
    return list;
  }, [allRanked, searchTerm, filterSponsor, filterStream, filterCategory, filterGender, filterState, profileByRoll]);"""

if old_all_ranked in content:
    content = content.replace(old_all_ranked, new_all_ranked)
else:
    print("Could not find allRanked")

# 2. Add the search-row above the All students rankwise table
old_table_header = """      <div className="card">
        <div className="section-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <Trophy size={14} aria-hidden="true" />
          All students rankwise — {selectedTestKey}
        </div>
        <div className="table-wrap" style={{ maxHeight: 440, overflowY: 'auto' }}>
          <table className="table table-compact">
            <thead>
              <tr>
                <th>Rank</th><th>Student</th><th>Cat.</th><th>Stream</th>"""

search_row = """
        <div className="search-row" style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '14px', marginBottom: '14px' }}>
          <div style={{ position: 'relative', flex: '1 1 200px' }}>
            <Search size={13} style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: 'var(--gray-400)', pointerEvents: 'none' }} />
            <input
              className="input"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by name or roll…"
              style={{ width: '100%', paddingLeft: 30 }}
            />
          </div>
          <select className="input select" value={filterSponsor} onChange={(e) => setFilterSponsor(e.target.value)} style={{ flex: '1 1 120px' }}>
            <option value="ALL">All Sponsors</option>
            {sponsorsList.filter((s) => s !== 'ALL' && s !== '—').map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
          <select className="input select" value={filterStream}   onChange={(e) => setFilterStream(e.target.value)}   style={{ flex: '1 1 120px' }}>
            <option value="ALL">All Streams</option>
            <option value="JEE">JEE</option>
            <option value="NEET">NEET</option>
          </select>
          <select className="input select" value={filterCategory} onChange={(e) => setFilterCategory(e.target.value)} style={{ flex: '1 1 120px' }}>
            {categories.map((c) => <option key={c} value={c}>{c === 'ALL' ? 'All Categories' : c}</option>)}
          </select>
          <select className="input select" value={filterGender} onChange={(e) => setFilterGender(e.target.value)} style={{ flex: '1 1 100px' }}>
            <option value="ALL">All Genders</option>
            {gendersList.filter((g) => g !== 'ALL').map((g) => <option key={g} value={g}>{g}</option>)}
          </select>
          <select className="input select" value={filterState} onChange={(e) => setFilterState(e.target.value)} style={{ flex: '1 1 120px' }}>
            <option value="ALL">All States</option>
            {statesList.filter((s) => s !== 'ALL').map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>"""

new_table_header = """      <div className="card">
        <div className="section-title" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <Trophy size={14} aria-hidden="true" />
          All students rankwise — {selectedTestKey}
        </div>""" + search_row + """
        <div className="table-wrap" style={{ maxHeight: 440, overflowY: 'auto' }}>
          <table className="table table-compact">
            <thead>
              <tr>
                <th>Rank</th><th>Student</th><th>Cat.</th><th>Stream</th>"""

if old_table_header in content:
    content = content.replace(old_table_header, new_table_header)
else:
    print("Could not find old_table_header")

# 3. Add Actions column header
old_actions_th = """                {rankingSubjects.map((s) => {
                  const abbr = s === 'Physics' ? 'P' : s === 'Chemistry' ? 'C' : (s === 'Math' || s === 'Mathematics') ? 'M' : s === 'Biology' ? 'B' : s.substring(0, 3);
                  return <th key={s} title={s}>{abbr}</th>;
                })}
                <th>Total</th>
              </tr>"""

new_actions_th = """                {rankingSubjects.map((s) => {
                  const abbr = s === 'Physics' ? 'P' : s === 'Chemistry' ? 'C' : (s === 'Math' || s === 'Mathematics') ? 'M' : s === 'Biology' ? 'B' : s.substring(0, 3);
                  return <th key={s} title={s}>{abbr}</th>;
                })}
                <th>Total</th>
                <th>Actions</th>
              </tr>"""

if old_actions_th in content:
    content = content.replace(old_actions_th, new_actions_th)
else:
    print("Could not find old_actions_th")

# 4. Use filteredRanked instead of allRanked in tbody and add action button
old_tbody = """              {allRanked.map((s) => {
                const profile = profileByRoll.get(s.roll);
                const photoUrl = profile?.['STUDENT PHOTO URL'] ? resolveStudentPhotoUrl(profile['STUDENT PHOTO URL'], 'fallback') : null;
                return (
                <tr key={`all-${s.roll}`} style={{ cursor: 'pointer' }} onClick={() => setViewingStudentId(s.roll)}>"""

new_tbody = """              {filteredRanked.map((s) => {
                const profile = profileByRoll.get(s.roll);
                const photoUrl = profile?.['STUDENT PHOTO URL'] ? resolveStudentPhotoUrl(profile['STUDENT PHOTO URL'], 'fallback') : null;
                return (
                <tr key={`all-${s.roll}`} style={{ cursor: 'pointer' }} onClick={() => setViewingStudentId(s.roll)}>"""

if old_tbody in content:
    content = content.replace(old_tbody, new_tbody)
else:
    print("Could not find old_tbody")

old_tr_end = """                  })}
                  <td><strong style={{ color: '#1a4fa0' }}>{s.marks}</strong></td>
                </tr>
              )})}
              {!allRanked.length && (
                <tr><td colSpan={4} style={{ textAlign: 'center', color: 'var(--gray-400)', padding: 20 }}>No data for {selectedTestKey}</td></tr>
              )}
            </tbody>"""

new_tr_end = """                  })}
                  <td><strong style={{ color: '#1a4fa0' }}>{s.marks}</strong></td>
                  <td>
                    <button
                      type="button"
                      className="btn btn-primary btn-sm"
                      aria-label="View student profile"
                      onClick={(e) => { e.stopPropagation(); setViewingStudentId(s.roll); }}
                    >
                      <Eye size={13} />
                    </button>
                  </td>
                </tr>
              )})}
              {!filteredRanked.length && (
                <tr><td colSpan={6} style={{ textAlign: 'center', color: 'var(--gray-400)', padding: 20 }}>No data found</td></tr>
              )}
            </tbody>"""

if old_tr_end in content:
    content = content.replace(old_tr_end, new_tr_end)
else:
    print("Could not find old_tr_end")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched CentreDashboard.jsx with shortlisting and Actions column")
