import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """          <div className="page-header-toolbar" style={{ marginLeft: 'auto', display: 'flex', gap: 12 }}>
            <select
              className="input select"
              value={selectedCenterCode}"""

new_code = """          <div className="page-header-toolbar" style={{ marginLeft: 'auto', display: activePage === 'leaderboard' ? 'none' : 'flex', gap: 12 }}>
            <select
              className="input select"
              value={selectedCenterCode}"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched CentreDashboard.jsx to hide toolbar on leaderboard tab")
else:
    print("Could not find old_code")
