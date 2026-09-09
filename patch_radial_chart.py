import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Update Recharts imports
content = content.replace(
    "import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';",
    "import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend, RadialBarChart, RadialBar, PolarAngleAxis } from 'recharts';"
)

# Build RadialBarChart placeholder
middle_col_old = """        {/* Middle Column: Placeholder for another Pie Chart */}
        <div style={{ background:'#fff', borderRadius:14, padding:'6px 8px', boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0', display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
          <SectionTitle Icon={PieChartIcon} color="#f59e0b">New Pie Chart</SectionTitle>
          <div style={{ flex: 1, minHeight: 180, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <span style={{ color: '#94a3b8', fontSize: 13 }}>Placeholder for Pie Chart</span>
          </div>
        </div>"""

middle_col_new = """        {/* Middle Column: Radial Progress Chart */}
        <div style={{ background:'#fff', borderRadius:14, padding:'6px 8px', boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0', display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
          <SectionTitle Icon={PieChartIcon} color="#f59e0b">Subject Performance</SectionTitle>
          <div style={{ flex: 1, minHeight: 180, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
            {(() => {
              const physicsAvg = Math.round(data.reduce((s, d) => s + (d.rawScores?.Physics||0), 0) / (data.length||1));
              const chemAvg = Math.round(data.reduce((s, d) => s + (d.rawScores?.Chemistry||0), 0) / (data.length||1));
              const mathAvg = Math.round(data.reduce((s, d) => s + (d.rawScores?.Math||d.rawScores?.Mathematics||0), 0) / (data.length||1));
              
              const radialData = [
                { name: 'Math', value: mathAvg, fill: '#ec4899' },
                { name: 'Chemistry', value: chemAvg, fill: '#8b5cf6' },
                { name: 'Physics', value: physicsAvg, fill: '#f59e0b' }
              ];
              const overallScore = Math.round((physicsAvg + chemAvg + mathAvg) / 3);

              return (
                <ResponsiveContainer width="100%" height={180}>
                  <RadialBarChart 
                    cx="50%" cy="50%" 
                    innerRadius="40%" outerRadius="90%" 
                    barSize={12} 
                    data={radialData}
                    startAngle={90} endAngle={-270}
                  >
                    <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
                    <RadialBar 
                      minAngle={15} 
                      background={{ fill: '#f1f5f9' }} 
                      clockWise={true} 
                      dataKey="value" 
                      cornerRadius={10}
                    />
                    <Tooltip cursor={{ fill: 'transparent' }} contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                    <Legend iconSize={8} layout="vertical" verticalAlign="middle" wrapperStyle={{ right: 0, fontSize: 10 }} />
                    <text x="50%" y="50%" textAnchor="middle" dominantBaseline="middle" style={{ fontSize: 24, fontWeight: 900, fill: '#1e293b' }}>
                      {overallScore}%
                    </text>
                    <text x="50%" y="65%" textAnchor="middle" dominantBaseline="middle" style={{ fontSize: 10, fontWeight: 600, fill: '#94a3b8' }}>
                      Average
                    </text>
                  </RadialBarChart>
                </ResponsiveContainer>
              );
            })()}
          </div>
        </div>"""

content = content.replace(middle_col_old, middle_col_new)

with open(filepath, 'w') as f:
    f.write(content)

print("Added RadialBarChart instead of Placeholder.")
