import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad_import = "import { LineChart, Line, XAxis, YAxis, CartesianGrid, Legend, ResponsiveContainer } from 'recharts';"
good_import = "import { LineChart, Line, XAxis, YAxis, CartesianGrid, Legend } from 'recharts';"

bad_render = """                  <div style={{ width: '100%', height: '70px' }}>
                    <ResponsiveContainer width="100%" height={100}>
                      <LineChart data={chartData} margin={{ top: 5, left: 0, bottom: -5, right: 10 }}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                        <XAxis dataKey="name" tick={{ fontSize: 8, fill: '#64748b' }} axisLine={false} tickLine={false} />
                        <YAxis reversed={isRank} domain={isRank ? [1, 'dataMax'] : [0, 'dataMax']} tick={{ fontSize: 8, fill: '#64748b' }} axisLine={false} tickLine={false} width={25} />
                        {subjects.map(sub => {
                          const dataKey = isRank ? `Rank_${sub.substring(0,3)}` : (metric === 'MARKS' ? sub : `${sub}_${metric.charAt(0).toUpperCase() + metric.slice(1).toLowerCase()}`);
                          return (
                            <Line key={sub} type="monotone" dataKey={dataKey} stroke={subjectColor(sub)} strokeWidth={1.5} dot={{ r: 1.5 }} isAnimationActive={false} />
                          );
                        })}
                        <Line type="monotone" dataKey={metric === 'MARKS' ? 'Total' : `Total_${metric.charAt(0).toUpperCase() + metric.slice(1).toLowerCase()}`} stroke="#1a4fa0" strokeWidth={2} dot={{ r: 2 }} isAnimationActive={false} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>"""

good_render = """                  <div style={{ width: '100%', height: '70px' }}>
                    <LineChart width={358} height={70} data={chartData} margin={{ top: 5, left: 0, bottom: -5, right: 10 }}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                      <XAxis dataKey="name" tick={{ fontSize: 8, fill: '#64748b' }} axisLine={false} tickLine={false} />
                      <YAxis reversed={isRank} domain={isRank ? [1, 'dataMax'] : [0, 'dataMax']} tick={{ fontSize: 8, fill: '#64748b' }} axisLine={false} tickLine={false} width={25} />
                      {subjects.map(sub => {
                        const dataKey = isRank ? `Rank_${sub.substring(0,3)}` : (metric === 'MARKS' ? sub : `${sub}_${metric.charAt(0).toUpperCase() + metric.slice(1).toLowerCase()}`);
                        return (
                          <Line key={sub} type="monotone" dataKey={dataKey} stroke={subjectColor(sub)} strokeWidth={1.5} dot={{ r: 1.5 }} isAnimationActive={false} />
                        );
                      })}
                      <Line type="monotone" dataKey={metric === 'MARKS' ? 'Total' : `Total_${metric.charAt(0).toUpperCase() + metric.slice(1).toLowerCase()}`} stroke="#1a4fa0" strokeWidth={2} dot={{ r: 2 }} isAnimationActive={false} />
                    </LineChart>
                  </div>"""

if bad_render in content:
    content = content.replace(bad_import, good_import)
    content = content.replace(bad_render, good_render)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Successfully patched StudentReportCard.jsx")
else:
    print("Could not find the target string!")

