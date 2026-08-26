import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Signature
content = content.replace(
    "export default function CentreLeaderboard({ centreStats = [], selTest, onCentreClick }) {",
    "export default function CentreLeaderboard({ centreStats = [], selTest, selectedSubject, onCentreClick }) {"
)

# 2. Sort Logic
old_sort = "  const sortedStats = [...centreStats].sort((a, b) => a.rank - b.rank);"
new_sort = """  const isQualSort = selectedSubject === 'Qualification';
  const sortedStats = [...centreStats].sort((a, b) => {
    if (isQualSort) return (b.qualRate || 0) - (a.qualRate || 0);
    return a.rank - b.rank;
  });
  const currentDataKey = isQualSort ? "qualRate" : "avg";
  const currentYLabel = isQualSort ? "Qualification %" : "Average Score";"""
content = content.replace(old_sort, new_sort)

# 3. renderCustomBarLabel text
old_text = "          {value}"
new_text = "          {value}{isQualSort ? '%' : ''}"
content = content.replace(old_text, new_text)

# 4. YAxis Label
old_ylabel = """            <Label value="Average Score" angle={-90} position="insideLeft" style={{ textAnchor: 'middle', fontSize: 16, fontWeight: 'bold', fill: '#64748b' }} />"""
new_ylabel = """            <Label value={currentYLabel} angle={-90} position="insideLeft" style={{ textAnchor: 'middle', fontSize: 16, fontWeight: 'bold', fill: '#64748b' }} />"""
content = content.replace(old_ylabel, new_ylabel)

# 5. Bar component
old_bar = """          <Bar isAnimationActive={false} 
            dataKey="avg" 
            radius={[4, 4, 0, 0]} 
            style={{ cursor: 'pointer' }} 
            fill="#1a4fa0"
            activeBar={{ fill: '#2563eb', stroke: '#93c5fd', strokeWidth: 2 }}"""
new_bar = """          <Bar isAnimationActive={false} 
            dataKey={currentDataKey}
            radius={[4, 4, 0, 0]} 
            style={{ cursor: 'pointer' }} 
            fill={isQualSort ? "#8b5cf6" : "#1a4fa0"}
            activeBar={{ fill: isQualSort ? "#a78bfa" : '#2563eb', stroke: isQualSort ? "#c4b5fd" : '#93c5fd', strokeWidth: 2 }}"""
content = content.replace(old_bar, new_bar)

# 6. LabelList
old_labellist = """<LabelList dataKey="avg" content={renderCustomBarLabel} />"""
new_labellist = """<LabelList dataKey={currentDataKey} content={renderCustomBarLabel} />"""
content = content.replace(old_labellist, new_labellist)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched CentreLeaderboard.jsx")
