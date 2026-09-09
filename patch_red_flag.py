import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """        <KpiCard icon={Award}    value={qualRate !== null ? `${qualRate}%` : '—'} label="Overall Qual. Rate"
          sub={`${totalQualified} / ${totalAppeared} qualified`} bg="#f0fdf4" color="#16a34a"/>"""

new_code = """        <KpiCard 
          icon={(qualRate !== null && qualRate < 80) ? Flag : Award}    
          value={qualRate !== null ? `${qualRate}%` : '—'} 
          label="Overall Qual. Rate"
          sub={`${totalQualified} / ${totalAppeared} qualified`} 
          bg={(qualRate !== null && qualRate < 80) ? "#fef2f2" : "#f0fdf4"} 
          color={(qualRate !== null && qualRate < 80) ? "#ef4444" : "#16a34a"}
        />"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("Code patched successfully!")
else:
    print("Old code not found!")

with open(filepath, 'w') as f:
    f.write(content)

