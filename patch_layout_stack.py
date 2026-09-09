import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Update the grid template columns
content = content.replace(
    "<div style={{ display: 'grid', gridTemplateColumns: centreBoard.length > 0 ? 'repeat(3, minmax(0, 1fr))' : '1fr', gap: 20 }}>",
    "<div style={{ display: 'grid', gridTemplateColumns: centreBoard.length > 0 ? 'minmax(0, 1.2fr) minmax(0, 1fr)' : '1fr', gap: 20 }}>\n        {/* Left Column: Stacked Students & Centres */}\n        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>"
)

# 2. Update Top 5 Students to remove height: 100% and flex since it's now stacked and shouldn't stretch unnecessarily
content = content.replace(
    "boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e8f0fc', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>",
    "boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e8f0fc' }}>"
)

# 3. Change the logic for Right Column wrapping
# Currently, it looks like:
#       {/* Right Column: Top 10 Centres Cards & Pie Chart ── */}
#       {centreBoard.length > 0 && (() => {
#         const sorted = [...centreBoard].sort((a,b) => (b.avg||0)-(a.avg||0));
#         const overallAvg = sorted.reduce((sum, c) => sum + (c.avg||0), 0) / (sorted.length || 1);
#
#         return (
#           <>
#             {/* Left Column: Top and Bottom 5 */}
#             <div style={{ background:'#fff', borderRadius:14, padding:'12px 16px',
#               boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>

# We need to change this so Top/Bottom Centres is inside the stacked div, then close the stacked div, then open the pie chart div.
old_right_col = """      {/* Right Column: Top 10 Centres Cards & Pie Chart ── */}
      {centreBoard.length > 0 && (() => {
        const sorted = [...centreBoard].sort((a,b) => (b.avg||0)-(a.avg||0));
        const overallAvg = sorted.reduce((sum, c) => sum + (c.avg||0), 0) / (sorted.length || 1);

        return (
          <>
            {/* Left Column: Top and Bottom 5 */}
            <div style={{ background:'#fff', borderRadius:14, padding:'12px 16px',
              boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>"""

new_right_col = """      {/* Stacked Top 10 Centres ── */}
      {centreBoard.length > 0 && (() => {
        const sorted = [...centreBoard].sort((a,b) => (b.avg||0)-(a.avg||0));
        return (
            <div style={{ background:'#fff', borderRadius:14, padding:'12px 16px',
              boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0' }}>"""

content = content.replace(old_right_col, new_right_col)

# 4. Now find the transition from Top/Bottom Centres to Pie Chart
old_transition = """                  </>
                );
              })()}
            </div>
            
            {/* Right Column: Pie Chart */}
            <div style={{ background:'#fff', borderRadius:14, padding:'12px 16px',
              boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0', display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
              <SectionTitle Icon={PieChartIcon} color="#f59e0b">Centre Distribution</SectionTitle>"""

new_transition = """                  </>
                );
              })()}
            </div>
          );
        })()}
        </div> {/* Close Stacked Left Column */}
            
        {/* Right Column: Pie Chart */}
        {centreBoard.length > 0 && (() => {
            const sorted = [...centreBoard].sort((a,b) => (b.avg||0)-(a.avg||0));
            const overallAvg = sorted.reduce((sum, c) => sum + (c.avg||0), 0) / (sorted.length || 1);
            return (
            <div style={{ background:'#fff', borderRadius:14, padding:'12px 16px',
              boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0', display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
              <SectionTitle Icon={PieChartIcon} color="#f59e0b">Centre Distribution</SectionTitle>"""

content = content.replace(old_transition, new_transition)

# 5. Find the end of the Pie chart
# We had:
#             </div>
#           </>
#         );
#       })()}
#       </div>

old_end = """            </div>
          </>
        );
      })()}
    </div>
  );
}"""

new_end = """            </div>
          );
      })()}
    </div>
  );
}"""

content = content.replace(old_end, new_end)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated layout to stack Top 5 Students and Top/Bottom Centres in the left column")
