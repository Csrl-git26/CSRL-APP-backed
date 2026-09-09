import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """      {centreBoard.length > 0 && (() => {
        const sorted = [...centreBoard].sort((a,b) => (b.avg||0)-(a.avg||0));
        const overallAvg = sorted.reduce((sum, c) => sum + (c.avg||0), 0) / (sorted.length || 1);
        const aboveAvgCount = sorted.filter(c => (c.avg||0) >= overallAvg).length;
        const belowAvgCount = sorted.filter(c => (c.avg||0) < overallAvg).length;

        const pieData = [
          { name: 'Above Average', value: aboveAvgCount, color: '#10b981' },
          { name: 'Below Average', value: belowAvgCount, color: '#ef4444' }
        ];

        return (
          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 20 }}>"""

new_block = """      {centreBoard.length > 0 && (() => {
        const sorted = [...centreBoard].sort((a,b) => (b.avg||0)-(a.avg||0));
        const overallAvg = sorted.reduce((sum, c) => sum + (c.avg||0), 0) / (sorted.length || 1);

        return (
          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 20 }}>"""

if old_block in content:
    content = content.replace(old_block, new_block)
else:
    print("old_block not found")

old_pie = """                <ResponsiveContainer width="100%" height={220}>
                  <PieChart>
                    <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={50} outerRadius={70} paddingAngle={2}>
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value, name) => [`${value} Centres`, name]} contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                    <Legend verticalAlign="bottom" height={36} iconType="circle" wrapperStyle={{ fontSize: 12, paddingTop: 10 }} />
                  </PieChart>
                </ResponsiveContainer>"""

new_pie = """                <ResponsiveContainer width="100%" height={220}>
                  <PieChart>
                    <Pie 
                      data={sorted} 
                      dataKey="avg" 
                      nameKey="code" 
                      cx="50%" 
                      cy="50%" 
                      innerRadius={40} 
                      outerRadius={70} 
                      paddingAngle={1}
                      label={({ cx, cy, midAngle, outerRadius, name }) => {
                        const RADIAN = Math.PI / 180;
                        const radius = outerRadius + 12;
                        const x = cx + radius * Math.cos(-midAngle * RADIAN);
                        const y = cy + radius * Math.sin(-midAngle * RADIAN);
                        return (
                          <text x={x} y={y} fill="#64748b" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central" fontSize={10}>
                            {name}
                          </text>
                        );
                      }}
                      labelLine={false}
                    >
                      {sorted.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={(entry.avg||0) >= overallAvg ? '#10b981' : '#ef4444'} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value, name) => [Math.round(value), `Centre ${name}`]} contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                    <Legend 
                      verticalAlign="bottom" 
                      height={36} 
                      iconType="circle" 
                      wrapperStyle={{ fontSize: 12, paddingTop: 10 }} 
                      payload={[
                        { value: 'Above Average', type: 'circle', color: '#10b981' },
                        { value: 'Below Average', type: 'circle', color: '#ef4444' }
                      ]}
                    />
                  </PieChart>
                </ResponsiveContainer>"""

if old_pie in content:
    content = content.replace(old_pie, new_pie)
else:
    print("old_pie not found")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched InsightsDashboard.jsx successfully")
