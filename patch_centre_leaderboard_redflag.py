import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Patch 1: Tooltip signature and isRedFlag
old_tooltip = """const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    const centerName = CENTERS[data.code]?.name || data.code;
    const isRedFlag = data.avg < 100 || (data.qualRate ?? 0) < 50;"""

new_tooltip = """const CustomTooltip = ({ active, payload, selectedSubject }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    const centerName = CENTERS[data.code]?.name || data.code;
    
    let isRedFlag = false;
    if (selectedSubject === 'Total' || !selectedSubject) {
      isRedFlag = data.avg < 100 || (data.qualRate ?? 0) < 50;
    } else if (selectedSubject === 'Qualification') {
      isRedFlag = (data.qualRate ?? 0) < 50;
    } else {
      isRedFlag = data.avg <= 20;
    }"""

if old_tooltip in content:
    content = content.replace(old_tooltip, new_tooltip)
else:
    print("Could not find tooltip target")
    sys.exit(1)

# Patch 2: renderCustomBarLabel signature and isRedFlag
old_label = """    const renderCustomBarLabel = (props) => {
    const { x, y, width, height, value, index } = props;
    const data = sortedStats[index];
    const isRedFlag = data && (data.avg < 100 || (data.qualRate ?? 0) < 50);"""

new_label = """    const renderCustomBarLabel = (props) => {
    const { x, y, width, height, value, index } = props;
    const data = sortedStats[index];
    
    let isRedFlag = false;
    if (data) {
      if (selectedSubject === 'Total' || !selectedSubject) {
        isRedFlag = data.avg < 100 || (data.qualRate ?? 0) < 50;
      } else if (selectedSubject === 'Qualification') {
        isRedFlag = (data.qualRate ?? 0) < 50;
      } else {
        isRedFlag = data.avg <= 20;
      }
    }"""

if old_label in content:
    content = content.replace(old_label, new_label)
else:
    print("Could not find label target")
    sys.exit(1)

# Patch 3: Tooltip usage in BarChart
old_tooltip_render = "<Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(0,0,0,0.05)' }} />"
new_tooltip_render = "<Tooltip content={<CustomTooltip selectedSubject={selectedSubject} />} cursor={{ fill: 'rgba(0,0,0,0.05)' }} />"

if old_tooltip_render in content:
    content = content.replace(old_tooltip_render, new_tooltip_render)
else:
    print("Could not find tooltip render target")
    sys.exit(1)

with open(filepath, 'w') as f:
    f.write(content)
print("Successfully patched CentreLeaderboard red flags!")
