import re
import os

files = [
    '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx',
    '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx',
    '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
]

old_span_12 = "<span style={{ display: 'inline-block', width: 12, height: 12, borderRadius: '50%', background: '#cc0000', animation: 'csrlPulse 1.2s ease-out infinite', boxShadow: '0 0 0 0 rgba(220,0,0,1)', flexShrink: 0, border: '2px solid #ff0000' }} />"
old_span_14 = "<span style={{ display: 'inline-block', width: 14, height: 14, borderRadius: '50%', background: '#cc0000', animation: 'csrlPulse 1.2s ease-out infinite', boxShadow: '0 0 0 0 rgba(220,0,0,1)', flexShrink: 0, border: '2px solid #ff0000' }} />"

new_flag = "<Flag size={14} color=\"#cc0000\" fill=\"#cc0000\" style={{ animation: 'csrlPulse 1.2s ease-out infinite', flexShrink: 0 }} />"

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Check if Flag is imported
        if 'import' in content and 'lucide-react' in content and 'Flag' not in content:
            # simple inject Flag into lucide-react import
            content = re.sub(r"import \{(.*?)\} from 'lucide-react';", lambda m: "import {" + m.group(1) + ", Flag} from 'lucide-react';", content)
        
        content = content.replace(old_span_12, new_flag)
        content = content.replace(old_span_14, new_flag)

        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"Patched {filepath}")

