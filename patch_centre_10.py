import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Change limits
old_limits = """      fetchRankings(null, { testKey: selectedTestKey, centerCode: selectedCenterCode, limit: 30, order: 'desc' }).catch(() => ({ ranked: [] })),
      fetchRankings(null, { testKey: selectedTestKey, centerCode: selectedCenterCode, limit: 30, order: 'asc'  }).catch(() => ({ ranked: [] })),"""
new_limits = """      fetchRankings(null, { testKey: selectedTestKey, centerCode: selectedCenterCode, limit: 10, order: 'desc' }).catch(() => ({ ranked: [] })),
      fetchRankings(null, { testKey: selectedTestKey, centerCode: selectedCenterCode, limit: 10, order: 'asc'  }).catch(() => ({ ranked: [] })),"""
if old_limits in content:
    content = content.replace(old_limits, new_limits)
    print("Patched limits")
else:
    print("Failed to patch limits")

# Change Top 30 title
old_top_title = "Top 30 — {selectedTestKey}"
new_top_title = "Top 10 — {selectedTestKey}"
if old_top_title in content:
    content = content.replace(old_top_title, new_top_title)
    print("Patched Top 30 title")
else:
    print("Failed to patch Top 30 title")

# Change Bottom 30 title
old_bottom_title = "Bottom 30 — {selectedTestKey}"
new_bottom_title = "Bottom 10 — {selectedTestKey}"
if old_bottom_title in content:
    content = content.replace(old_bottom_title, new_bottom_title)
    print("Patched Bottom 30 title")
else:
    print("Failed to patch Bottom 30 title")

with open(filepath, 'w') as f:
    f.write(content)
