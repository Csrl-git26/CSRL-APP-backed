import sys

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentDashboard.jsx', 'r') as f:
    content = f.read()

# 1. Add RANK to buttons
content = content.replace(
    "{['MARKS', 'ACCURACY', 'ATTEMPTED', 'CORRECT'].map((m) => (",
    "{['MARKS', 'ACCURACY', 'ATTEMPTED', 'CORRECT', 'RANK'].map((m) => ("
)

# 2. Update YAxis
content = content.replace(
    "<YAxis domain={[0, 'dataMax']} axisLine={{ stroke: 'var(--gray-300)' }} tickLine={false} tick={{ fill: 'var(--gray-500)', fontSize: 11 }} width={55} />",
    "<YAxis reversed={chartMetric === 'RANK'} domain={chartMetric === 'RANK' ? [1, 'dataMax'] : [0, 'dataMax']} axisLine={{ stroke: 'var(--gray-300)' }} tickLine={false} tick={{ fill: 'var(--gray-500)', fontSize: 11 }} width={55} />"
)

# 3. Update Tooltip
content = content.replace(
    "if (chartMetric === 'CORRECT') return [value ?? '—', `${subName} Correct`];",
    "if (chartMetric === 'CORRECT') return [value ?? '—', `${subName} Correct`];\n                    if (chartMetric === 'RANK') return [value ?? '—', `${subName} Rank`];"
)

# 4. Update Subject Line dataKey
content = content.replace(
    "if (chartMetric === 'CORRECT') dataKey = `${sub}_Correct`;",
    "if (chartMetric === 'CORRECT') dataKey = `${sub}_Correct`;\n                  if (chartMetric === 'RANK') dataKey = `${sub}_Rank`;"
)

# 5. Update Total Line dataKey
content = content.replace(
    "dataKey={chartMetric === 'MARKS' ? 'Total' : `Total_${chartMetric.charAt(0).toUpperCase() + chartMetric.slice(1).toLowerCase()}`}",
    "dataKey={chartMetric === 'MARKS' ? 'Total' : (chartMetric === 'RANK' ? 'Total_Rank' : `Total_${chartMetric.charAt(0).toUpperCase() + chartMetric.slice(1).toLowerCase()}`)}"
)

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentDashboard.jsx', 'w') as f:
    f.write(content)
