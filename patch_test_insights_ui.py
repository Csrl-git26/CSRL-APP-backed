import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestInsightsPanel.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_ui = """        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 12 }}>
          <select
            className="input select"
            value={rankMode}
            onChange={(e) => setRankMode(e.target.value)}
            style={{ maxWidth: 200 }}
          >
            <option value="all">All students</option>
            <option value="top10">Top 10 students</option>
            <option value="bottom10">Lowest 10 students</option>
          </select>
          <select
            className="input select"
            value={sortOrder}
            onChange={(e) => setSortOrder(e.target.value)}
            style={{ maxWidth: 200 }}
          >
            <option value="desc">Sort: Highest first</option>
            <option value="asc">Sort: Lowest first</option>
          </select>
          <select
            className="input select"
            value={selectedCenter}
            onChange={(e) => setSelectedCenter(e.target.value)}
            style={{ maxWidth: 220 }}
          >
            <option value="ALL">All centres</option>
            {centerOptions.map((c) => (
              <option key={c} value={c}>{centreLabel(c)}</option>
            ))}
          </select>
        </div>"""

new_ui = """        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 12 }}>
          <select className="input select" value={rankMode} onChange={(e) => setRankMode(e.target.value)} style={{ maxWidth: 200 }}>
            <option value="all">All students</option>
            <option value="top10">Top 10 students</option>
            <option value="bottom10">Lowest 10 students</option>
          </select>
          <select className="input select" value={sortOrder} onChange={(e) => setSortOrder(e.target.value)} style={{ maxWidth: 200 }}>
            <option value="desc">Sort: Highest first</option>
            <option value="asc">Sort: Lowest first</option>
          </select>
          <select className="input select" value={selectedCenter} onChange={(e) => setSelectedCenter(e.target.value)} style={{ maxWidth: 220 }}>
            <option value="ALL">All centres</option>
            {centerOptions.map((c) => (
              <option key={c} value={c}>{centreLabel(c)}</option>
            ))}
          </select>
          
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
          <select className="input select" value={filterCategory} onChange={(e) => setFilterCategory(e.target.value)} style={{ flex: '1 1 120px' }}>
            {categories.map((c) => <option key={c} value={c}>{c === 'ALL' ? 'All Categories' : c}</option>)}
          </select>
          <select className="input select" value={filterGender} onChange={(e) => setFilterGender(e.target.value)} style={{ flex: '1 1 100px' }}>
            <option value="ALL">All Genders</option>
            {gendersList.filter((g) => g !== 'ALL').map((g) => <option key={g} value={g}>{g}</option>)}
          </select>
        </div>"""

old_table = """            <thead>
              <tr>
                <th>#</th>
                <th>Student</th>
                <th>Centre</th>
                <th>Total</th>
              </tr>
            </thead>
            <tbody>
              {filteredRanked.map((r) => (
                <tr key={r.roll}>
                  <td><strong>{r.rank}</strong></td>
                  <td>
                    <div style={{ fontWeight: 600 }}>{r.name}</div>
                    <div style={{ fontSize: 11, color: 'var(--gray-400)' }}>{r.roll}</div>
                  </td>
                  <td>{r.center}</td>
                  <td><strong style={{ color: '#1a4fa0' }}>{r.marks}</strong></td>
                </tr>
              ))}
              {!filteredRanked.length && (
                <tr>
                  <td colSpan={4} style={{ textAlign: 'center', color: 'var(--gray-400)', padding: 20 }}>
                    No data
                  </td>
                </tr>
              )}
            </tbody>"""

new_table = """            <thead>
              <tr>
                <th>#</th>
                <th>Student</th>
                <th>Centre</th>
                <th>Total</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredRanked.map((r) => (
                <tr key={r.roll} style={{ cursor: onViewStudent ? 'pointer' : 'default' }} onClick={() => onViewStudent && onViewStudent(r.roll)}>
                  <td><strong>{r.rank}</strong></td>
                  <td>
                    <div className="student-row">
                      {r.photo ? (
                        <img src={r.photo.startsWith('http') ? r.photo : `https://example.com/fallback`} alt="Avatar" className="avatar" style={{width: 32, height: 32, fontSize: 12, objectFit: 'cover'}} />
                      ) : (
                        <div className="avatar" style={{width: 32, height: 32, fontSize: 12}}>{r.name ? r.name.substring(0, 2).toUpperCase() : 'ST'}</div>
                      )}
                      <div>
                        <div style={{ fontWeight: 600 }}>{r.name}</div>
                        <div style={{ fontSize: 11, color: 'var(--gray-400)' }}>{r.roll}</div>
                      </div>
                    </div>
                  </td>
                  <td>{r.center}</td>
                  <td><strong style={{ color: '#1a4fa0' }}>{r.marks}</strong></td>
                  <td>
                    {onViewStudent && (
                      <button
                        type="button"
                        className="btn btn-primary btn-sm"
                        aria-label="View student profile"
                        onClick={(e) => { e.stopPropagation(); onViewStudent(r.roll); }}
                      >
                        <Eye size={13} />
                      </button>
                    )}
                  </td>
                </tr>
              ))}
              {!filteredRanked.length && (
                <tr>
                  <td colSpan={5} style={{ textAlign: 'center', color: 'var(--gray-400)', padding: 20 }}>
                    No data found
                  </td>
                </tr>
              )}
            </tbody>"""

content = content.replace(old_ui, new_ui)
content = content.replace(old_table, new_table)

with open(filepath, 'w') as f:
    f.write(content)

print("Patched UI!")
