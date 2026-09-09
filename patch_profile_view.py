import re

# Patch AdminDashboard.jsx
filepath_admin = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath_admin, 'r') as f:
    content_admin = f.read()

old_call = "<StudentProfileView profile={finalProfile} studentTests={studentTests} testColumns={data.testColumns} />"
new_call = "<StudentProfileView profile={finalProfile} studentTests={studentTests} testColumns={data.testColumns} hidePersonalDetails={true} />"

if old_call in content_admin:
    content_admin = content_admin.replace(old_call, new_call)
    with open(filepath_admin, 'w') as f:
        f.write(content_admin)
    print("Patched AdminDashboard.jsx")
else:
    print("WARNING: Could not find StudentProfileView call in AdminDashboard.jsx")

# Patch StudentProfileView.jsx
filepath_profile = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx'
with open(filepath_profile, 'r') as f:
    content_profile = f.read()

old_sig = "export default function StudentProfileView({ profile, studentTests, testColumns, isHiddenForBulk = false, prefetchedChart = null, prefetchedWeakTopics = null }) {"
new_sig = "export default function StudentProfileView({ profile, studentTests, testColumns, isHiddenForBulk = false, prefetchedChart = null, prefetchedWeakTopics = null, hidePersonalDetails = false }) {"

if old_sig in content_profile:
    content_profile = content_profile.replace(old_sig, new_sig)
else:
    print("WARNING: Could not find StudentProfileView signature")

# Wrap the grid-2 containing Personal and Education Info
old_grid = """      <div className="grid-2">
        <div className="card">
          <div className="section-title">👨‍👩‍👧 Personal & Selection Info</div>"""

new_grid = """      {!hidePersonalDetails && (
      <div className="grid-2">
        <div className="card">
          <div className="section-title">👨‍👩‍👧 Personal & Selection Info</div>"""

# Find where to close it
old_grid_end = """          )}
        </div>
      </div>

      {/* Target & Analysis */}"""

new_grid_end = """          )}
        </div>
      </div>
      )}

      {/* Target & Analysis */}"""

if old_grid in content_profile and old_grid_end in content_profile:
    content_profile = content_profile.replace(old_grid, new_grid)
    content_profile = content_profile.replace(old_grid_end, new_grid_end)
else:
    print("WARNING: Could not find grid-2 block to replace")

with open(filepath_profile, 'w') as f:
    f.write(content_profile)

print("Patched StudentProfileView.jsx")
