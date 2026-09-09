import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Current top-level grid:
# <div style={{ display: 'grid', gridTemplateColumns: centreBoard.length > 0 ? 'repeat(3, minmax(0, 1fr))' : '1fr', gap: 20 }}>

# 1. Change to 2 columns: 1.5fr and 1fr (or 1fr 1fr)
content = content.replace(
    "<div style={{ display: 'grid', gridTemplateColumns: centreBoard.length > 0 ? 'repeat(3, minmax(0, 1fr))' : '1fr', gap: 20 }}>",
    "<div style={{ display: 'grid', gridTemplateColumns: centreBoard.length > 0 ? 'minmax(0, 1.3fr) minmax(0, 1fr)' : '1fr', gap: 20 }}>"
)

# 2. We need to wrap Top 5 Students and Top/Bottom Centres in a single div column.
# Let's find where Top 5 Students starts:
# {/* Left Column: Top 5 Students */}
content = content.replace(
    "{/* Left Column: Top 5 Students */}",
    "{/* Left Column: Stacked Students & Centres */}\n        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>\n          {/* Top 5 Students */}"
)

# 3. We need to find where the Right Column (Pie Chart) starts, and close the stacked div right before it.
# Wait, currently the layout is:
# <div style={{ display: 'grid', ... }}>
#   <div style={{ background: '#fff' ...}}> (Top 5 students) </div>
#   {centreBoard.length > 0 && (() => { ... return (<> <div...>(Top/Bottom Centres)</div> <div...>(Pie Chart)</div> </>) })()}
# </div>

# This means Top/Bottom Centres is generated dynamically in the right block.
# Let's change the structure. We can just move the Top/Bottom Centres rendering up, or move Top 5 Students into the dynamic block.
