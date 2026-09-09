import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Shrink global SectionTitle margin
content = content.replace("marginBottom:14", "marginBottom:6")

# Shrink the outer padding of Top 5 Students
content = content.replace(
    "padding:'12px 16px',\n          boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e8f0fc'",
    "padding:'6px 8px',\n          boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e8f0fc'"
)

# Shrink the outer padding of Top 10 Centres
content = content.replace(
    "padding:'12px 16px',\n              boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0'",
    "padding:'6px 8px',\n              boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0'"
)

with open(filepath, 'w') as f:
    f.write(content)

print("Super shrunk the outer paddings and title margins.")
