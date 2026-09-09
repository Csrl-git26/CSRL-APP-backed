import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Reduce padding of the 3 main column containers
content = content.replace("padding:'18px 20px'", "padding:'12px 16px'")

# 2. Reduce RankRow spacing
# padding:'8px 10px' -> '4px 8px'
content = content.replace("padding:'8px 10px'", "padding:'4px 8px'")
# gap: 6 inside RankRow text -> gap: 2
content = content.replace("display: 'flex', flexDirection: 'column', gap: 6, justifyContent: 'center'", "display: 'flex', flexDirection: 'column', gap: 2, justifyContent: 'center'")
# marginBottom:4 in RankRow -> marginBottom: 2
content = content.replace("marginBottom:4, border:'none'", "marginBottom:2, border:'none'")

# 3. Reduce Top/Bottom 5 Centres cards
# padding:'8px 6px' -> '6px 4px'
content = content.replace("padding:'8px 6px', borderRadius:8", "padding:'6px 4px', borderRadius:8")
# gap:10 for the grids -> gap:6
content = content.replace("display:'grid', gridTemplateColumns:'repeat(5,1fr)', gap:10", "display:'grid', gridTemplateColumns:'repeat(5,1fr)', gap:6")
# bottomCentres.length > 0 ? 20 : 0 -> ? 10 : 0
content = content.replace("bottomCentres.length > 0 ? 20 : 0", "bottomCentres.length > 0 ? 12 : 0")

# 4. Reduce Pie Chart height
content = content.replace("minHeight: 280", "minHeight: 220")
content = content.replace("height={280}", "height={220}")
content = content.replace("innerRadius={65}", "innerRadius={50}")
content = content.replace("outerRadius={90}", "outerRadius={75}")

with open(filepath, 'w') as f:
    f.write(content)
print("Updated InsightsDashboard layout to reduce vertical space")
