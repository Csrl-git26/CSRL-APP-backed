import re

# 1. Update index.css
index_path = '/Users/surya/Desktop/CSRL-APP-frontend/src/index.css'
with open(index_path, 'r') as f:
    content = f.read()

# The content padding might be 'padding: 24px;'
content = content.replace('.content { padding: 24px; }', '.content { padding: 12px 24px; }')
with open(index_path, 'w') as f:
    f.write(content)


# 2. Update AdminDashboard.jsx
admin_path = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(admin_path, 'r') as f:
    admin = f.read()

# In LeaderboardSection:
admin = admin.replace(
    "display: 'flex', justifyContent: 'flex-end', marginBottom: 16",
    "display: 'flex', justifyContent: 'flex-end', marginBottom: 8"
)
admin = admin.replace(
    "marginBottom: 32",
    "marginBottom: 12"
)
# And the page-header in AdminDashboard.jsx?
# Let's check where the tabs are rendered. It's usually in a .page-header
# AdminDashboard renders a header with tabs. Let's see if there's any big margin there.

with open(admin_path, 'w') as f:
    f.write(admin)


# 3. Update InsightsDashboard.jsx
insights_path = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(insights_path, 'r') as f:
    insights = f.read()

# KPI cards container
insights = insights.replace(
    "display:'flex', gap:12, marginBottom:16",
    "display:'flex', gap:12, marginBottom:8"
)
# KPI card padding
insights = insights.replace(
    "padding:'10px 14px'",
    "padding:'6px 12px'"
)
# Also Pie Chart height: from 220 down to 180!
insights = insights.replace("minHeight: 220", "minHeight: 180")
insights = insights.replace("height={220}", "height={180}")
insights = insights.replace("innerRadius={50}", "innerRadius={45}")
insights = insights.replace("outerRadius={75}", "outerRadius={65}")

with open(insights_path, 'w') as f:
    f.write(insights)

print("Applied aggressive vertical compression across the app.")
