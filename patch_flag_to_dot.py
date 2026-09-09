import os

files_to_patch = [
    '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx',
    '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
]

old_tag = '<Flag size={14} fill="currentColor" strokeWidth={2.5} />'
# Adjust size slightly for inline text if needed, 10 or 12px might be better, let's stick to 12px for the header badge.
new_tag = '<span style={{ display: \'inline-block\', width: 12, height: 12, borderRadius: \'50%\', background: \'#cc0000\', animation: \'csrlPulse 1.2s ease-out infinite\', boxShadow: \'0 0 0 0 rgba(220,0,0,1)\', flexShrink: 0, border: \'2px solid #ff0000\' }} />'

for filepath in files_to_patch:
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()

    new_content = content.replace(old_tag, new_tag)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Patched {os.path.basename(filepath)}")
    else:
        print(f"No changes for {os.path.basename(filepath)}")
