import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Change title color
content = content.replace(
    '<SectionTitle Icon={PieChartIcon} color="#10b981">Top 5 Centres Qual %</SectionTitle>',
    '<SectionTitle Icon={PieChartIcon} color="#f59e0b">Top 5 Centres Qual %</SectionTitle>'
)

# Add onClick and fix tooltip
old_radial = """                    <RadialBar 
                      minAngle={15} 
                      background={{ fill: '#f1f5f9' }} 
                      clockWise={true} 
                      dataKey="value" 
                      cornerRadius={10}
                      label={{ position: 'insideStart', fill: '#fff', fontSize: 9, fontWeight: 700, formatter: (val) => `${val}%` }}
                    />
                    <Tooltip 
                      cursor={{ fill: 'transparent' }} 
                      contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', fontSize: 12, fontWeight: 600 }} 
                      formatter={(val) => [`${val}%`, 'Qual Rate']}
                    />"""

new_radial = """                    <RadialBar 
                      minAngle={15} 
                      background={{ fill: '#f1f5f9' }} 
                      clockWise={true} 
                      dataKey="value" 
                      cornerRadius={10}
                      label={{ position: 'insideStart', fill: '#fff', fontSize: 9, fontWeight: 700, formatter: (val) => `${val}%` }}
                      onClick={(data, index) => { if (onViewCentre && data && data.name) { onViewCentre(data.name); } else if (onViewCentre && data && data.payload && data.payload.name) { onViewCentre(data.payload.name); } }}
                      style={{ cursor: 'pointer' }}
                    />
                    <Tooltip 
                      cursor={{ fill: 'transparent' }} 
                      contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)', fontSize: 12, fontWeight: 600 }} 
                      formatter={(val, name, props) => [`${val}%`, props?.payload?.name || 'Qual Rate']}
                    />"""

content = content.replace(old_radial, new_radial)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated RadialBar click handler and title color.")
