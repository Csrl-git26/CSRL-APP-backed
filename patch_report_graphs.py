import sys

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx', 'r') as f:
    content = f.read()

# 1. Replace the single chart with 4 charts
graph_start = content.find("{/* FULL WIDTH: Performance Graph */}")
graph_end = content.find("      {/* FULL WIDTH: Overall Weak Topics MOVED TO PAGE 2 */}")

metrics = [
    {'key': 'MARKS', 'title': 'Marks Trend', 'totalKey': 'Total'},
    {'key': 'ATTEMPTED', 'title': 'Attempted Trend', 'suffix': '_Attempted', 'totalKey': 'Total_Attempted'},
    {'key': 'ACCURACY', 'title': 'Accuracy Trend', 'suffix': '_Accuracy', 'totalKey': 'Total_Accuracy', 'format': '%'},
    {'key': 'RANK', 'title': 'Rank Trend', 'suffix': '_Rank', 'totalKey': 'Total_Rank', 'reversed': 'true'}
]

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
                  <div style={{ fontSize: '11px', fontWeight: 700, color: '#475569', marginBottom: '4px', textAlign: 'center' }}>{titles[metric]}</div>
                  <div style={{ width: '100%', height: '140px' }}>
                    <ResponsiveContainer width={360} height={140}>
                      <LineChart data={chartData} margin={{ top: 10, left: 0, bottom: 0, right: 10 }}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                        <XAxis dataKey="name" tick={{ fontSize: 8, fill: '#64748b' }} axisLine={false} tickLine={false} />
                        <YAxis reversed={isRank} domain={isRank ? [1, 'dataMax'] : [0, 'dataMax']} tick={{ fontSize: 8, fill: '#64748b' }} axisLine={false} tickLine={false} width={25} />
                        {subjects.map(sub => {
                          const dataKey = metric === 'MARKS' ? sub : `${sub}_${metric.charAt(0).toUpperCase() + metric.slice(1).toLowerCase()}`;
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
      </div>

"""

if graph_start != -1 and graph_end != -1:
    content = content[:graph_start] + four_graphs_code + content[graph_end:]

# 2. Merge Page 1 and Page 2
page2_start = content.find("    </div>\n    \n    {/* PAGE 2: Performance Table */}\n    <div id=\"pdf-report-page2\"")
page2_header_end = content.find("      <h3 style={{ fontSize: '14px'", page2_start)

if page2_start != -1 and page2_header_end != -1:
    # Just remove everything from page2_start up to page2_header_end,
    # except we need to keep the closing div of the whole component if it existed...
    # Wait, page2_start starts with `    </div>`. This was closing `pdf-report-content`.
    # We want to REMOVE that `</div>` so the content continues inside `pdf-report-content`.
    content = content[:page2_start] + "\n\n" + content[page2_header_end:]

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx', 'w') as f:
    f.write(content)
print("Patched successfully")
