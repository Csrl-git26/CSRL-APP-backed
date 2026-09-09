import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Revert shadow
content = content.replace("boxShadow:'0 8px 30px rgba(0,0,0,0.04)'", "boxShadow:'0 2px 8px rgba(0,0,0,0.07)'")

# Revert Pie props
old_pie = """                    <Pie 
                      data={sorted} 
                      dataKey="avg" 
                      nameKey="code" 
                      cx="50%" 
                      cy="50%" 
                      innerRadius={65} 
                      outerRadius={90} 
                      paddingAngle={3}
                      cornerRadius={6}
                      stroke="none"
                      isAnimationActive={true}"""

new_pie = """                    <Pie 
                      data={sorted} 
                      dataKey="avg" 
                      nameKey="code" 
                      cx="50%" 
                      cy="50%" 
                      innerRadius={65} 
                      outerRadius={90} 
                      paddingAngle={1}"""

if old_pie in content:
    content = content.replace(old_pie, new_pie)
else:
    print("old_pie not found")


# Remove center text div
old_center_text = """                {/* Center Text */}
                <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -60%)', textAlign: 'center', pointerEvents: 'none' }}>
                  <div style={{ fontSize: 10, color: '#94a3b8', fontWeight: 600, textTransform: 'uppercase', letterSpacing: 1 }}>Avg Score</div>
                  <div style={{ fontSize: 24, fontWeight: 800, color: '#1e293b', marginTop: -2 }}>{Math.round(overallAvg)}</div>
                </div>"""

if old_center_text in content:
    content = content.replace(old_center_text + "\n", "")
else:
    print("old_center_text not found")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched InsightsDashboard.jsx successfully")
