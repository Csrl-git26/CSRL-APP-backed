filepath = '../CSRL-APP-frontend/src/components/PerformanceChart.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_subjects = """  const subjects = streamCfg.subjects.filter((sub) => chartData.some((row) => 
    row[sub] !== undefined && row[sub] !== null
  ));"""

new_subjects = """  const subjects = (streamCfg?.subjects || []).filter((sub) => (chartData || []).some((row) => 
    row[sub] !== undefined && row[sub] !== null
  ));"""

if old_subjects in content:
    content = content.replace(old_subjects, new_subjects)
    print("Patched PerformanceChart: null-guarded subjects and chartData")
else:
    print("ERROR: could not find subjects block in PerformanceChart.jsx")
    print("Actual line:", content[content.find("subjects = stream"):content.find("subjects = stream")+200])

with open(filepath, 'w') as f:
    f.write(content)
