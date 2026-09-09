import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Make shadow more prominent
content = content.replace("boxShadow:'0 2px 8px rgba(0,0,0,0.07)'", "boxShadow:'0 8px 30px rgba(0,0,0,0.04)'")

# Add corner radius and padding angle to pie
old_pie_start = """                    <Pie 
                      data={sorted} 
                      dataKey="avg" 
                      nameKey="code" 
                      cx="50%" 
                      cy="50%" 
                      innerRadius={55} 
                      outerRadius={85} 
                      paddingAngle={1}"""

new_pie_start = """                    <Pie 
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

if old_pie_start in content:
    content = content.replace(old_pie_start, new_pie_start)
else:
    print("old_pie_start not found")

# Add a centered text using absolute positioning inside the ResponsiveContainer's wrapper
old_resp_wrapper = """              <div style={{ flex: 1, minHeight: 280, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                <ResponsiveContainer width="100%" height={280}>"""

new_resp_wrapper = """              <div style={{ flex: 1, minHeight: 280, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
                {/* Center Text */}
                <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -60%)', textAlign: 'center', pointerEvents: 'none' }}>
                  <div style={{ fontSize: 10, color: '#94a3b8', fontWeight: 600, textTransform: 'uppercase', letterSpacing: 1 }}>Avg Score</div>
                  <div style={{ fontSize: 24, fontWeight: 800, color: '#1e293b', marginTop: -2 }}>{Math.round(overallAvg)}</div>
                </div>
                <ResponsiveContainer width="100%" height={280}>"""

if old_resp_wrapper in content:
    content = content.replace(old_resp_wrapper, new_resp_wrapper)
else:
    print("old_resp_wrapper not found")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched InsightsDashboard.jsx successfully")
