import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Remove the search input UI from CentreDashboard.jsx
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
if old_search_ui in content:
    content = content.replace(old_search_ui, "")
    with open(filepath, 'w') as f:
        f.write(content)
    print("Removed Search UI from CentreDashboard")
else:
    print("Search UI not found in CentreDashboard")
