import os

data_service = '/Users/surya/Desktop/CSRL-APP-frontend/src/services/dataService.js'
with open(data_service, 'r') as f:
    content = f.read()

# Patch dataService.js
old_fetchOverview = """export async function fetchOverview(_token, centerCode) {
  const qs = centerCode ? `?centerCode=${encodeURIComponent(centerCode)}` : '';
  return apiFetch(`/api/analytics/overview${qs}`);
}"""

new_fetchOverview = """export async function fetchOverview(_token, centerCode, stream) {
  const params = new URLSearchParams();
  if (centerCode) params.set('centerCode', centerCode);
  if (stream && stream !== 'ALL') params.set('stream', stream);
  const qs = params.toString() ? `?${params.toString()}` : '';
  return apiFetch(`/api/analytics/overview${qs}`);
}"""

if old_fetchOverview in content:
    content = content.replace(old_fetchOverview, new_fetchOverview)
    with open(data_service, 'w') as f:
        f.write(content)
    print("Patched dataService.js successfully")
else:
    print("Could not find fetchOverview in dataService.js (might already be patched)")

admin_dash = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(admin_dash, 'r') as f:
    content = f.read()

# Patch AdminDashboard.jsx fetchOverview
old_admin_overview = """fetchOverview(null).then(setOverview).catch(() => null);
  }, [refreshTrigger]);"""

new_admin_overview = """fetchOverview(null, null, stream).then(setOverview).catch(() => null);
  }, [refreshTrigger, stream]);"""

if old_admin_overview in content:
    content = content.replace(old_admin_overview, new_admin_overview)
    print("Patched fetchOverview in AdminDashboard.jsx")
else:
    print("Could not find fetchOverview use effect in AdminDashboard.jsx")

# Patch AdminDashboard.jsx fetchRankings
old_admin_rankings = """fetchRankings(null, { testKey: combinedKey, limit: 15, order: 'desc' }).catch(() => ({ ranked: [] })),
      fetchRankings(null, { testKey: combinedKey, limit: 15, order: 'asc'  }).catch(() => ({ ranked: [] })),
    ]).then(([top, bottom]) => {
      setTopRanked(top.ranked    || []);
      setBottomRanked(bottom.ranked || []);
    });
  }, [selectedTestKey, selectedSubject, refreshTrigger]);"""

new_admin_rankings = """fetchRankings(null, { testKey: combinedKey, limit: 15, order: 'desc', stream }).catch(() => ({ ranked: [] })),
      fetchRankings(null, { testKey: combinedKey, limit: 15, order: 'asc', stream }).catch(() => ({ ranked: [] })),
    ]).then(([top, bottom]) => {
      setTopRanked(top.ranked    || []);
      setBottomRanked(bottom.ranked || []);
    });
  }, [selectedTestKey, selectedSubject, refreshTrigger, stream]);"""

if old_admin_rankings in content:
    content = content.replace(old_admin_rankings, new_admin_rankings)
    print("Patched fetchRankings in AdminDashboard.jsx")
else:
    print("Could not find fetchRankings use effect in AdminDashboard.jsx")

with open(admin_dash, 'w') as f:
    f.write(content)

centre_dash = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(centre_dash, 'r') as f:
    content = f.read()

old_centre_overview = """fetchOverview(null, selectedCenterCode).catch(() => null),"""
new_centre_overview = """fetchOverview(null, selectedCenterCode, globalStream).catch(() => null),"""

if old_centre_overview in content:
    content = content.replace(old_centre_overview, new_centre_overview)
    # Also fix the dependency array for overview in CentreDashboard
    # It might just be in the same useEffect as the other fetch calls.
    with open(centre_dash, 'w') as f:
        f.write(content)
    print("Patched fetchOverview in CentreDashboard.jsx")
else:
    print("Could not find fetchOverview in CentreDashboard.jsx")

print("All done!")
