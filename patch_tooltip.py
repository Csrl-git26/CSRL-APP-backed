import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_tooltip = """<Tooltip formatter={(value, name) => [Math.round(value), `Centre ${name}`]} contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />"""

new_tooltip = """<Tooltip 
                      content={({ active, payload }) => {
                        if (active && payload && payload.length) {
                          const data = payload[0].payload;
                          const isAbove = (data.avg || 0) >= overallAvg;
                          return (
                            <div style={{ background: '#fff', padding: '8px 12px', borderRadius: 8, boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
                              <span style={{ color: isAbove ? '#3b82f6' : '#ef4444', fontWeight: 600, fontSize: 13 }}>
                                Centre {payload[0].name}
                              </span>
                            </div>
                          );
                        }
                        return null;
                      }}
                    />"""

if old_tooltip in content:
    content = content.replace(old_tooltip, new_tooltip)
else:
    print("old_tooltip not found")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched InsightsDashboard.jsx successfully")
