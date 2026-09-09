import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Change grid template to 3 columns
content = content.replace(
    "gridTemplateColumns: centreBoard.length > 0 ? 'minmax(0, 1.2fr) minmax(0, 1fr)' : '1fr'",
    "gridTemplateColumns: centreBoard.length > 0 ? 'minmax(0, 1.2fr) minmax(0, 1fr) minmax(0, 1fr)' : '1fr'"
)

# Insert the middle column
middle_col_code = """        </div> {/* Close Stacked Left Column */}
            
        {/* Middle Column: Placeholder for another Pie Chart */}
        <div style={{ background:'#fff', borderRadius:14, padding:'6px 8px', boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0', display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
          <SectionTitle Icon={PieChartIcon} color="#f59e0b">New Pie Chart</SectionTitle>
          <div style={{ flex: 1, minHeight: 180, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <span style={{ color: '#94a3b8', fontSize: 13 }}>Placeholder for Pie Chart</span>
          </div>
        </div>

        {/* Right Column: Pie Chart */}"""

content = content.replace(
    "        </div> {/* Close Stacked Left Column */}\n            \n        {/* Right Column: Pie Chart */}",
    middle_col_code
)

with open(filepath, 'w') as f:
    f.write(content)

print("Inserted a middle column placeholder for a new pie chart.")
