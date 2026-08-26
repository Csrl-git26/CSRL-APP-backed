import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_select = """            </select>
            <select
              className="input select"
              value={selectedTestKey}
              onChange={(e) => setSelectedTestKey(e.target.value)}
              style={{ background: 'rgba(255,255,255,.15)', color: '#fff', borderColor: 'rgba(255,255,255,.3)', width: 200 }}
            >
              {rankingTestColumns.map((t) => <option key={t} value={t} style={{ color: '#333' }}>{t === 'ALL_FMT' ? 'All FMT Average' : t}</option>)}
            </select>
          </div>"""

new_select = """            </select>
            {['topbottom'].includes(activePage) && (
              <select
                className="input select"
                value={selectedTestKey}
                onChange={(e) => setSelectedTestKey(e.target.value)}
                style={{ background: 'rgba(255,255,255,.15)', color: '#fff', borderColor: 'rgba(255,255,255,.3)', width: 200 }}
              >
                {rankingTestColumns.map((t) => <option key={t} value={t} style={{ color: '#333' }}>{t === 'ALL_FMT' ? 'All FMT Average' : t}</option>)}
              </select>
            )}
          </div>"""

if old_select in content:
    content = content.replace(old_select, new_select)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched dropdown visibility successfully!")
else:
    print("Could not find old_select in CentreDashboard.jsx")
