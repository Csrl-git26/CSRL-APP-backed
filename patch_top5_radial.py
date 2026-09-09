import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """          <SectionTitle Icon={PieChartIcon} color="#f59e0b">Subject Performance</SectionTitle>
          <div style={{ flex: 1, minHeight: 180, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
            {(() => {
              const safeData = Array.isArray(data) ? data : [];
              const physicsAvg = Math.round(safeData.reduce((s, d) => s + (d.rawScores?.Physics||0), 0) / (safeData.length||1));
              const chemAvg = Math.round(safeData.reduce((s, d) => s + (d.rawScores?.Chemistry||0), 0) / (safeData.length||1));
              const mathAvg = Math.round(safeData.reduce((s, d) => s + (d.rawScores?.Math||d.rawScores?.Mathematics||0), 0) / (safeData.length||1));
              
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
          </div>"""

new_code = """          <SectionTitle Icon={PieChartIcon} color="#10b981">Top 5 Centres Qual %</SectionTitle>
          <div style={{ flex: 1, minHeight: 180, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
            {(() => {
              if (!centreBoard || centreBoard.length === 0) return <div>No Data</div>;
              const top5Qual = [...centreBoard].sort((a,b) => (b.qualRate||0) - (a.qualRate||0)).slice(0, 5);
              
              const colors = ['#10b981', '#3b82f6', '#f59e0b', '#ec4899', '#8b5cf6'];
              // Reverse so the #1 rank is on the outermost ring
              const radialData = top5Qual.map((c, i) => ({
                name: c.code,
                value: Math.round(c.qualRate || 0),
                fill: colors[i % colors.length]
              })).reverse();
              
              const avgQual = Math.round(top5Qual.reduce((s, c) => s + (c.qualRate||0), 0) / (top5Qual.length||1));

              return (
                <ResponsiveContainer width="100%" height={180}>
                  <RadialBarChart 
                    cx="50%" cy="50%" 
                    innerRadius="30%" outerRadius="90%" 
                    barSize={10} 
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
                    <Tooltip 
                      cursor={{ fill: 'transparent' }} 
                      contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', fontSize: 12, fontWeight: 600 }} 
                      formatter={(val) => [`${val}%`, 'Qual Rate']}
                    />
                    <Legend iconSize={8} layout="vertical" verticalAlign="middle" wrapperStyle={{ right: 0, fontSize: 10 }} />
                    <text x="50%" y="50%" textAnchor="middle" dominantBaseline="middle" style={{ fontSize: 24, fontWeight: 900, fill: '#1e293b' }}>
                      {avgQual}%
                    </text>
                    <text x="50%" y="65%" textAnchor="middle" dominantBaseline="middle" style={{ fontSize: 10, fontWeight: 600, fill: '#94a3b8' }}>
                      Top 5 Avg
                    </text>
                  </RadialBarChart>
                </ResponsiveContainer>
              );
            })()}
          </div>"""

content = content.replace(old_code, new_code)

with open(filepath, 'w') as f:
    f.write(content)

print("Changed RadialBarChart to show Top 5 Centres by Qualification Rate")
