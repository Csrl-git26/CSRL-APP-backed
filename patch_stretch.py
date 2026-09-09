import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Left Column (Top 5 Students)
content = content.replace(
    "boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e8f0fc', alignSelf: 'start' }}>",
    "boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e8f0fc', height: '100%', display: 'flex', flexDirection: 'column' }}>"
)

# Right Column child 1 (Top / Bottom Centres)
content = content.replace(
    "boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0' }}>",
    "boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0', height: '100%', display: 'flex', flexDirection: 'column' }}>"
)

# Right Column child 2 (Centre Distribution)
# Wait, child 2 already has display: 'flex', flexDirection: 'column'. Let's just add height: '100%' if missing.
content = content.replace(
    "boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0', display: 'flex', flexDirection: 'column' }}>",
    "boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0', display: 'flex', flexDirection: 'column', height: '100%' }}>"
)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated flex container to stretch to equal height")
