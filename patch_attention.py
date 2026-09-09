import os

files_to_patch = [
    '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx',
    '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx',
    '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx',
    '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
]

for filepath in files_to_patch:
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()

    new_content = content.replace('ACTION REQUIRED', 'ATTENTION').replace('Action Required', 'Attention')
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Patched {os.path.basename(filepath)}")
    else:
        print(f"No changes for {os.path.basename(filepath)}")
