import sys

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx', 'r') as f:
    content = f.read()

# 1. Replace the single chart with 4 charts
graph_start = content.find("      {/* FULL WIDTH: Performance Graph */}")
graph_end = content.find("      {/* FULL WIDTH: Overall Weak Topics MOVED TO PAGE 2 */}")

four_graphs_code = """      {/* FULL WIDTH: Performance Graphs */}
      <div style={{ background: '#f8fafc', padding: '12px', borderRadius: '8px', border: '1px solid #e2e8f0', marginBottom: '12px' }}>
        <h3 style={{ fontSize: '14px', fontWeight: 800, color: '#0f172a', textTransform: 'uppercase', marginBottom: '8px', borderBottom: '1px solid #cbd5e1', paddingBottom: '4px' }}>
          Performance Trends
        </h3>
        
        {chartData && chartData.length > 0 ? (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
            {['MARKS', 'ATTEMPTED', 'ACCURACY', 'RANK'].map(metric => {
              const titles = { MARKS: 'Marks', ATTEMPTED: 'Attempted', ACCURACY: 'Accuracy (%)', RANK: 'Rank' };
              const isRank = metric === 'RANK';
              const isAcc = metric === 'ACCURACY';
              
              return (
                <div key={metric} style={{ background: '#fff', border: '1px solid #e2e8f0', borderRadius: '6px', padding: '8px' }}>
                  <div style={{ fontSize: '11px', fontWeight: 700, color: '#475569', marginBottom: '4px', textAlign: 'center', textTransform: 'uppercase' }}>{titles[metric]} Trend</div>
                  <div style={{ width: '100%', height: '150px' }}>
                    <ResponsiveContainer width="100%" height={150}>
                      <LineChart data={chartData} margin={{ top: 10, left: -25, bottom: 0, right: 10 }}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                        <XAxis dataKey="name" tick={{ fontSize: 8, fill: '#64748b' }} axisLine={false} tickLine={false} />
                        <YAxis reversed={isRank} domain={isRank ? [1, 'dataMax'] : [0, 'dataMax']} tick={{ fontSize: 8, fill: '#64748b' }} axisLine={false} tickLine={false} width={25} />
                        {subjects.map(sub => {
                          let dataKey = sub;
                          if (metric === 'ATTEMPTED') dataKey = `${sub}_Attempted`;
                          if (metric === 'ACCURACY') dataKey = `${sub}_Accuracy`;
                          if (metric === 'RANK') dataKey = `${sub}_Rank`;
                          return (
                            <Line key={sub} type="monotone" dataKey={dataKey} stroke={subjectColor(sub)} strokeWidth={1.5} dot={{ r: 1.5 }} isAnimationActive={false} />
                          );
                        })}
                        <Line type="monotone" dataKey={metric === 'MARKS' ? 'Total' : `Total_${metric.charAt(0).toUpperCase() + metric.slice(1).toLowerCase()}`} stroke="#1a4fa0" strokeWidth={2} dot={{ r: 2 }} isAnimationActive={false} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div style={{ textAlign: 'center', color: '#94a3b8', padding: '20px' }}>No performance data available</div>
        )}
      </div>\n\n"""

if graph_start != -1 and graph_end != -1:
    content = content[:graph_start] + four_graphs_code + content[graph_end:]


# 2. Remove Page 2 break & headers
page_break_str = """      {/* FULL WIDTH: Overall Weak Topics MOVED TO PAGE 2 */}

    </div>
    
    {/* PAGE 2: Performance Table */}
    <div id="pdf-report-page2" style={{
      width: '800px',
      background: 'white',
      padding: '24px',
      color: '#0f172a',
      fontFamily: 'Inter, sans-serif'
    }}>
      {/* HEADER */}
      <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '3px solid #1a4fa0', paddingBottom: '8px', marginBottom: '16px' }}>
        <div>
          <h1 style={{ fontSize: '24px', fontWeight: 900, color: '#1a4fa0', margin: 0, textTransform: 'uppercase' }}>
            CSRL Student Report (Page 2)
          </h1>
        </div>
        <div style={{ textAlign: 'right' }}>
          <h2 style={{ fontSize: '20px', fontWeight: 800, margin: 0, color: '#1e293b' }}>{profile["STUDENT'S NAME"] || 'Unknown'}</h2>
        </div>
      </div>"""

if page_break_str in content:
    content = content.replace(page_break_str, "")

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx', 'w') as f:
    f.write(content)
print("Patched successfully")
