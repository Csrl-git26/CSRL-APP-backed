import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Add import
old_import = "import PastYearDataTab from './PastYearDataTab';"
new_import = """import PastYearDataTab from './PastYearDataTab';
import InsightsDashboard from './InsightsDashboard';"""

if old_import in content:
    content = content.replace(old_import, new_import)
    print("Added InsightsDashboard import!")
else:
    print("WARNING: Could not add import")

# 2. Add 'insights' tab to ALL_TABS (first position for prominence)
old_tabs = """const ALL_TABS = [
  { key: 'leaderboard', Icon: Trophy,         label: 'Centre Leaderboard' },
  { key: 'centre-overview', Icon: Building2, label: 'Centre Overview'      },
  { key: 'ranking',     Icon: TrendingUp,      label: 'Rankings'           },
  { key: 'pastyear',    Icon: Package,         label: 'Past Year Data'     },
  { key: 'import',      Icon: Upload,          label: 'Import / Export'    },
];"""

new_tabs = """const ALL_TABS = [
  { key: 'insights',    Icon: Lightbulb,       label: 'Insights'           },
  { key: 'leaderboard', Icon: Trophy,          label: 'Centre Leaderboard' },
  { key: 'centre-overview', Icon: Building2,   label: 'Centre Overview'    },
  { key: 'ranking',     Icon: TrendingUp,      label: 'Rankings'           },
  { key: 'pastyear',    Icon: Package,         label: 'Past Year Data'     },
  { key: 'import',      Icon: Upload,          label: 'Import / Export'    },
];"""

if old_tabs in content:
    content = content.replace(old_tabs, new_tabs)
    print("Added insights tab to ALL_TABS!")
else:
    print("WARNING: Could not update ALL_TABS")

# 3. Render InsightsDashboard when activePage === 'insights'
old_render = "          {activePage === 'leaderboard' && LeaderboardSection()}"
new_render = """          {activePage === 'insights'    && <InsightsDashboard data={data} overview={overview} topRanked={topRanked} bottomRanked={bottomRanked} centreBoard={centreBoard} selectedTestKey={selectedTestKey} />}
          {activePage === 'leaderboard' && LeaderboardSection()}"""

if old_render in content:
    content = content.replace(old_render, new_render)
    print("Added Insights render!")
else:
    print("WARNING: Could not add insights render")

with open(filepath, 'w') as f:
    f.write(content)

print("Done! AdminDashboard.jsx updated.")
