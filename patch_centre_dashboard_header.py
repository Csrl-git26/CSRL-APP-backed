import sys
filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_toolbar_start = '<div className="page-header-toolbar" style={{ marginLeft: \'auto\', display: \'flex\', gap: 12 }}>'
new_toolbar_start = '{activePage !== \'leaderboard\' && (\n          <div className="page-header-toolbar" style={{ marginLeft: \'auto\', display: \'flex\', gap: 12 }}>'

# We need to wrap the whole toolbar div in {activePage !== 'leaderboard' && ( ... )}
# Let's find the closing div of page-header-toolbar.

# It looks like this:
'''          <div className="page-header-toolbar" style={{ marginLeft: 'auto', display: 'flex', gap: 12 }}>
            <select
              className="input select"
              value={selectedCenterCode}
...
              {allTestOptions.map((t) => <option key={t} value={t} style={{ color: '#333' }}>{t}</option>)}
            </select>
          </div>'''

# Actually there are two places: one is when adminViewCenterCode is false, and one might be different?
# Wait, let's use sed to see lines 990-1025.
