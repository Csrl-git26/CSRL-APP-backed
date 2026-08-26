import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """            {['topbottom'].includes(activePage) && (
              <select
                className="input select"
                value={selectedTestKey}
                onChange={(e) => setSelectedTestKey(e.target.value)}
                style={{ background: 'rgba(255,255,255,.15)', color: '#fff', borderColor: 'rgba(255,255,255,.3)', width: 200 }}
              >
                {rankingTestColumns.map((t) => <option key={t} value={t} style={{ color: '#333' }}>{t === 'ALL_FMT' ? 'All FMT Average' : t}</option>)}
              </select>
            )}"""

new_block = """            <select
              className="input select"
              value={selectedTestKey}
              onChange={(e) => setSelectedTestKey(e.target.value)}
              style={{ background: 'rgba(255,255,255,.15)', color: '#fff', borderColor: 'rgba(255,255,255,.3)', width: 200 }}
            >
              {rankingTestColumns.map((t) => <option key={t} value={t} style={{ color: '#333' }}>{t === 'ALL_FMT' ? 'All FMT Average' : t}</option>)}
            </select>"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Restored dropdown successfully!")
else:
    print("Could not find old_block in CentreDashboard.jsx")
