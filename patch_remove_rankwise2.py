import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

start_str = '      <div className="card">\n        <div className="section-title" style={{ display: \'flex\', alignItems: \'center\', gap: 6 }}>\n          <Trophy size={14} aria-hidden="true" />\n          All students rankwise — {selectedTestKey}\n        </div>'
end_str = '      <div className="card" style={{ marginTop: 8 }}>\n        <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 16, color: \'var(--csrl-blue)\' }}>Test Analysis Tab</h2>'

if start_str in content and end_str in content:
    start_idx = content.find(start_str)
    end_idx = content.find(end_str)
    
    new_content = content[:start_idx] + content[end_idx:]
    with open(filepath, 'w') as f:
        f.write(new_content)
    print("Patched successfully")
else:
    print("Could not find start or end strings")
