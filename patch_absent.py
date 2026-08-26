import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # We need to replace `|| '-'` with `|| 'Absent'` in the fmtRanks map
    # In AdminDashboard.jsx
    content = content.replace("m.fmtRanks?.[t] || '-'", "m.fmtRanks?.[t] || 'Absent'")
    # In CentreDashboard.jsx
    content = content.replace("s.fmtRanks?.[t] || '-'", "s.fmtRanks?.[t] || 'Absent'")

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

patch_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx')
patch_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx')
