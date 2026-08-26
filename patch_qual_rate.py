import sys

def replace_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # CentreLeaderboard replacements
    if 'CentreLeaderboard' in filepath:
        content = content.replace("isRedFlag = data.avg < 100 || (data.qualRate ?? 0) < 50;", "isRedFlag = data.avg < 100 || (data.qualRate ?? 0) < 80;")
        content = content.replace("isRedFlag = (data.qualRate ?? 0) < 50;", "isRedFlag = (data.qualRate ?? 0) < 80;")
        content = content.replace("color: data.qualRate < 50 ? '#ef4444' : 'var(--gray-700)'", "color: data.qualRate < 80 ? '#ef4444' : 'var(--gray-700)'")
        content = content.replace("fontWeight: data.qualRate < 50 ? 700 : 600", "fontWeight: data.qualRate < 80 ? 700 : 600")

    # AdminDashboard and CentreDashboard replacements for qualPct
    if 'AdminDashboard' in filepath or 'CentreDashboard' in filepath:
        content = content.replace("qualPct < 50 ?", "qualPct < 80 ?")

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Patched {filepath}")

replace_in_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx')
replace_in_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx')
replace_in_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx')
