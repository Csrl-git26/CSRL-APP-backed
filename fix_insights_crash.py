filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# The bad block: renderQualCardSide accidentally placed inside SectionTitle
# We need to remove lines 24-96 (the entire renderQualCardSide function body)
bad = """
  const renderQualCardSide = (isBottom5) => {
    return (
      <div className="card" style={{ display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between', backfaceVisibility: 'hidden', padding: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <SectionTitle Icon={PieChartIcon} color="#2563eb">
            {isBottom5 ? (stream === 'NEET' ? 'BOTTOM 5 CENTRE - MBBS' : 'BOTTOM 5 CENTRE - QUAL') : (stream === 'NEET' ? 'TOP 5 CENTRE - MBBS %' : 'TOP 5 CENTRE - QUAL %')}
          </SectionTitle>
          <div \n            onClick={(e) => { e.stopPropagation(); setShowBottom5Qual(!showBottom5Qual); }}\n            className="flip-button-3d" style={{ padding: 0, width: 24, height: 24, minHeight: 0 }}\n            title={`Flip to ${isBottom5 ? 'Top' : 'Bottom'} 5`}\n          >\n            <Repeat size={12} color="#64748b" strokeWidth={2.5} />\n          </div>\n        </div>\n        <div style={{ flex: 1, minHeight: 180, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>\n          {(() => {\n            if (!centreBoard || centreBoard.length === 0) return <div>No Data</div>;\n            const sortedByQual = [...centreBoard].sort((a,b) => (b.qualRate||0) - (a.qualRate||0));\n            const top5Qual = isBottom5 ? sortedByQual.slice(-5) : sortedByQual.slice(0, 5);\n            \n            const colors = isBottom5 ? ["#c2410c", "#ea580c", "#f97316", "#fb923c", "#fdba74"] : ["#1d4ed8", "#2563eb", "#3b82f6", "#60a5fa", "#93c5fd"];\n            const radialData = top5Qual.map((c, i) => {\n              const rank = sortedByQual.findIndex(x => x.code === c.code) + 1;\n              return { name: c.code, value: Math.round(c.qualRate || 0), fill: colors[i % colors.length], rank };\n            }).reverse();\n            \n            const legendPayload = top5Qual.map((c, i) => {\n              const rank = sortedByQual.findIndex(x => x.code === c.code) + 1;\n              return { value: `${rank}. ${c.code}`, type: 'square', color: colors[i % colors.length] };\n            });\n\n            return (\n              <ResponsiveContainer width="100%" height={180}>\n                <RadialBarChart \n                  cx="40%" cy="50%" innerRadius="30%" outerRadius="90%" barSize={10} \n                  data={radialData} startAngle={90} endAngle={-270}\n                >\n                  <defs>\n                    <linearGradient id="bar3DVertical" x1="0" y1="0" x2="1" y2="0">\n                      <stop offset="0%" stopColor="#ffffff" stopOpacity={0.4} />\n                      <stop offset="30%" stopColor="#ffffff" stopOpacity={0.1} />\n                      <stop offset="100%" stopColor="#000000" stopOpacity={0.2} />\n                    </linearGradient>\n                  </defs>\n                  <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />\n                  <RadialBar \n                    isAnimationActive={true} animationDuration={2000} animationEasing="ease-out" minAngle={15} background={{ fill: '#f1f5f9' }} clockWise={true} dataKey="value" \n                    shape={(props) => renderRadialBarShape(props, activeRadialIndex, onViewCentre, setActiveRadialIndex)}\n                    label={{ position: 'insideStart', fill: '#fff', fontSize: 9, fontWeight: 700, formatter: (val) => `${val}%`, pointerEvents: 'none' }}\n                  />\n                  <Legend \n                    layout="vertical" verticalAlign="middle" wrapperStyle={{ right: 0 }} \n                    content={(props) => (\n                      <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>\n                        {legendPayload.map((entry, index) => (\n                          <li key={`item-${index}`} style={{ display: 'flex', alignItems: 'center', marginBottom: 4, fontSize: 11, color: '#1e3a8a', fontWeight: 900, textShadow: '0px 1px 1px rgba(255,255,255,0.9), 0px 1px 3px rgba(30,58,138,0.2)' }}>\n                            <span style={{ width: 8, height: 8, backgroundColor: entry.color, marginRight: 6, display: 'inline-block' }}></span>\n                            {entry.value}\n                          </li>\n                        ))}\n                      </ul>\n                    )}\n                  />\n                </RadialBarChart>\n              </ResponsiveContainer>\n            );\n          })()}\n        </div>\n      </div>\n    );\n  };"""

if "const renderQualCardSide" in content:
    # Use line-based approach: find line 25 to 96 range
    lines = content.split('\n')
    # Find the start: line with renderQualCardSide inside SectionTitle
    start_idx = None
    end_idx = None
    inside_section_title = False
    for i, line in enumerate(lines):
        if 'function SectionTitle(' in line:
            inside_section_title = True
        if inside_section_title and 'const renderQualCardSide' in line:
            start_idx = i
        if start_idx is not None and i > start_idx and line.strip() == '};':
            end_idx = i
            break

    if start_idx is not None and end_idx is not None:
        print(f"Found renderQualCardSide at lines {start_idx+1}-{end_idx+1}, removing...")
        # Remove those lines (replace with empty line)
        new_lines = lines[:start_idx] + lines[end_idx+1:]
        content = '\n'.join(new_lines)
        with open(filepath, 'w') as f:
            f.write(content)
        print("Fixed! Removed dead renderQualCardSide from SectionTitle.")
    else:
        print(f"Could not find block boundaries. start={start_idx}, end={end_idx}")
else:
    print("renderQualCardSide not found in file - already fixed?")
