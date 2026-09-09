import os

files = [
    '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx',
    '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx',
    '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
]

old_flag = "<Flag size={14} color=\"#cc0000\" fill=\"#cc0000\" style={{ animation: 'csrlPulse 1.2s ease-out infinite', flexShrink: 0 }} />"
new_flag = "<Flag size={14} color=\"#cc0000\" fill=\"#cc0000\" style={{ flexShrink: 0 }} />"

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        
        if old_flag in content:
            content = content.replace(old_flag, new_flag)
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"Patched {filepath}")
        else:
            print(f"Old flag not found in {filepath}")
