filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/PerformanceChart.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Upgrade the color palette to more vibrant/premium colors
content = content.replace(
    "const SUBJECT_COLORS = ['#3b82f6', '#f97316', '#22c55e', '#ef4444'];",
    "const SUBJECT_COLORS = ['#6366f1', '#f97316', '#10b981', '#f43f5e'];"
)

# 2. Soften the CartesianGrid
content = content.replace(
    '<CartesianGrid strokeDasharray="3 3" vertical={true} stroke="var(--gray-100)" />',
    '<CartesianGrid strokeDasharray="4 6" vertical={false} stroke="#e2e8f020" />'
)

# 3. Make subject lines thinner with smoother curve type
content = content.replace(
    """                <Line
                  key={sub}
                  name={sub}
                  type="monotone"
                  dataKey={dataKey}
                  stroke={SUBJECT_COLORS[i % SUBJECT_COLORS.length]}
                  strokeWidth={2.3}
                  dot={{ r: 3.5, strokeWidth: 1, fill: '#fff' }}
                  activeDot={{ r: 5 }}
                  connectNulls
                  isAnimationActive={false}
                  label={{ position: 'top', fill: SUBJECT_COLORS[i % SUBJECT_COLORS.length], fontSize: 11, fontWeight: 600, formatter: (val) => chartMetric === 'ACCURACY' && val !== null && val !== undefined ? `${val}%` : val }}
                />""",
    """                <Line
                  key={sub}
                  name={sub}
                  type="monotone"
                  dataKey={dataKey}
                  stroke={SUBJECT_COLORS[i % SUBJECT_COLORS.length]}
                  strokeWidth={1.8}
                  dot={{ r: 3, strokeWidth: 1.5, fill: '#fff', stroke: SUBJECT_COLORS[i % SUBJECT_COLORS.length] }}
                  activeDot={{ r: 5, strokeWidth: 2, fill: '#fff', stroke: SUBJECT_COLORS[i % SUBJECT_COLORS.length] }}
                  connectNulls
                  isAnimationActive={true}
                  animationDuration={800}
                  animationEasing="ease-in-out"
                  label={{ position: 'top', fill: SUBJECT_COLORS[i % SUBJECT_COLORS.length], fontSize: 10, fontWeight: 700, formatter: (val) => chartMetric === 'ACCURACY' && val !== null && val !== undefined ? `${val}%` : val }}
                />"""
)

# 4. Make Total line thinner too but still slightly bolder
content = content.replace(
    """              <Line
                name="Total"
                type="monotone"
                dataKey={chartMetric === 'MARKS' ? 'Total' : (chartMetric === 'RANK' ? 'Total_Rank' : `Total_${chartMetric.charAt(0).toUpperCase() + chartMetric.slice(1).toLowerCase()}`)}
                stroke="#a21caf"
                strokeWidth={3}
                dot={{ r: 4, strokeWidth: 2, fill: '#fff' }}
                activeDot={{ r: 6 }}
                connectNulls
                isAnimationActive={false}
                label={{ position: 'top', fill: '#a21caf', fontSize: 11, fontWeight: 700, formatter: (val) => chartMetric === 'ACCURACY' && val !== null && val !== undefined ? `${val}%` : val }}
              />""",
    """              <Line
                name="Total"
                type="monotone"
                dataKey={chartMetric === 'MARKS' ? 'Total' : (chartMetric === 'RANK' ? 'Total_Rank' : `Total_${chartMetric.charAt(0).toUpperCase() + chartMetric.slice(1).toLowerCase()}`)}
                stroke="#8b5cf6"
                strokeWidth={2.2}
                dot={{ r: 3.5, strokeWidth: 2, fill: '#fff', stroke: '#8b5cf6' }}
                activeDot={{ r: 6, strokeWidth: 2, fill: '#fff', stroke: '#8b5cf6' }}
                connectNulls
                isAnimationActive={true}
                animationDuration={1000}
                animationEasing="ease-in-out"
                label={{ position: 'top', fill: '#8b5cf6', fontSize: 10, fontWeight: 700, formatter: (val) => chartMetric === 'ACCURACY' && val !== null && val !== undefined ? `${val}%` : val }}
              />"""
)

# 5. Improve tooltip styling
content = content.replace(
    "contentStyle={{ background: '#fff', border: '1px solid var(--gray-100)', borderRadius: 8, fontSize: 12 }}",
    "contentStyle={{ background: 'rgba(255,255,255,0.95)', backdropFilter: 'blur(8px)', border: '1px solid #e2e8f0', borderRadius: 10, fontSize: 12, boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }}"
)

# 6. Update the Total line checkbox accent color to match
content = content.replace(
    "style={{ accentColor: sub === 'Total' ? '#a21caf' : SUBJECT_COLORS[i % SUBJECT_COLORS.length] }}",
    "style={{ accentColor: sub === 'Total' ? '#8b5cf6' : SUBJECT_COLORS[i % SUBJECT_COLORS.length] }}"
)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated PerformanceChart with thinner lines and premium styling.")
