import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad_import = "import { LineChart, Line, XAxis, YAxis, CartesianGrid, Legend, ResponsiveContainer } from 'recharts';"
good_import = "import { LineChart, Line, XAxis, YAxis, CartesianGrid, Legend } from 'recharts';"

bad1 = """<ResponsiveContainer width="100%" height={100}>
                      <LineChart data={chartData} margin={{ top: 5, left: 0, bottom: -5, right: 10 }}>"""
good1 = """<LineChart width={358} height={70} data={chartData} margin={{ top: 5, left: 0, bottom: -5, right: 10 }}>"""

bad2 = """</LineChart>
                    </ResponsiveContainer>"""
good2 = """</LineChart>"""

content = content.replace(bad_import, good_import)
content = content.replace(bad1, good1)
content = content.replace(bad2, good2)

with open(filepath, 'w') as f:
    f.write(content)
print("Successfully patched StudentReportCard.jsx")
