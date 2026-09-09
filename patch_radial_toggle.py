import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Add useState import
content = content.replace(
    "import { useMemo } from 'react';",
    "import { useMemo, useState } from 'react';"
)

# Add state hook inside InsightsDashboard
content = content.replace(
    "export default function InsightsDashboard({ data, overview, topRanked, bottomRanked, centreBoard, selectedTestKey, onViewCentre }) {",
    "export default function InsightsDashboard({ data, overview, topRanked, bottomRanked, centreBoard, selectedTestKey, onViewCentre }) {\n  const [showBottom5Qual, setShowBottom5Qual] = useState(false);"
)

# Update Middle Column section
old_middle = """        {/* Middle Column: Radial Progress Chart */}
        <div style={{ background:'#fff', borderRadius:14, padding:'6px 8px', boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0', display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
          <SectionTitle Icon={PieChartIcon} color="#f59e0b">Top 5 Centres Qual %</SectionTitle>
          <div style={{ flex: 1, minHeight: 180, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
            {(() => {
              if (!centreBoard || centreBoard.length === 0) return <div>No Data</div>;
              const top5Qual = [...centreBoard].sort((a,b) => (b.qualRate||0) - (a.qualRate||0)).slice(0, 5);"""

new_middle = """        {/* Middle Column: Radial Progress Chart */}
        <div style={{ background:'#fff', borderRadius:14, padding:'6px 8px', boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e2e8f0', display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <SectionTitle Icon={PieChartIcon} color={showBottom5Qual ? "#dc2626" : "#f59e0b"}>
              {showBottom5Qual ? 'Bottom 5 Centres Qual %' : 'Top 5 Centres Qual %'}
            </SectionTitle>
            <span 
              onClick={() => setShowBottom5Qual(!showBottom5Qual)}
              style={{ fontSize: 10, fontWeight: 800, color: '#3b82f6', cursor: 'pointer', userSelect: 'none', padding: '2px 6px', background: '#eff6ff', borderRadius: 4, marginBottom: 6 }}
            >
              Show {showBottom5Qual ? 'Top 5' : 'Bottom 5'}
            </span>
          </div>
          <div style={{ flex: 1, minHeight: 180, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
            {(() => {
              if (!centreBoard || centreBoard.length === 0) return <div>No Data</div>;
              const sortedByQual = [...centreBoard].sort((a,b) => (b.qualRate||0) - (a.qualRate||0));
              const top5Qual = showBottom5Qual ? sortedByQual.slice(-5).reverse() : sortedByQual.slice(0, 5);"""

content = content.replace(old_middle, new_middle)

# Update the center text "Top 5 Avg" to be dynamic
content = content.replace(
    "Top 5 Avg",
    "{showBottom5Qual ? 'Bot 5 Avg' : 'Top 5 Avg'}"
)

with open(filepath, 'w') as f:
    f.write(content)

print("Added toggle state for Top/Bottom 5 Qualification Rate chart")
