filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Remove the 'insights' tab from ALL_TABS
old_tabs = """const ALL_TABS = [
  { key: 'insights',    Icon: Lightbulb,       label: 'Insights'           },
  { key: 'leaderboard', Icon: Trophy,          label: 'Centre Leaderboard' },
  { key: 'centre-overview', Icon: Building2,   label: 'Centre Overview'    },
  { key: 'ranking',     Icon: TrendingUp,      label: 'Rankings'           },
  { key: 'pastyear',    Icon: Package,         label: 'Past Year Data'     },
  { key: 'import',      Icon: Upload,          label: 'Import / Export'    },
];"""

new_tabs = """const ALL_TABS = [
  { key: 'leaderboard', Icon: Trophy,         label: 'Centre Leaderboard' },
  { key: 'centre-overview', Icon: Building2, label: 'Centre Overview'      },
  { key: 'ranking',     Icon: TrendingUp,      label: 'Rankings'           },
  { key: 'pastyear',    Icon: Package,         label: 'Past Year Data'     },
  { key: 'import',      Icon: Upload,          label: 'Import / Export'    },
];"""

if old_tabs in content:
    content = content.replace(old_tabs, new_tabs)
    print("Removed insights tab from ALL_TABS!")
else:
    print("WARNING: Could not find ALL_TABS to restore")

# 2. Remove the standalone insights render line
old_insights_render = """          {activePage === 'insights'    && <InsightsDashboard data={data} overview={overview} topRanked={topRanked} bottomRanked={bottomRanked} centreBoard={centreBoard} selectedTestKey={selectedTestKey} />}
          {activePage === 'leaderboard' && LeaderboardSection()}"""

new_insights_render = "          {activePage === 'leaderboard' && LeaderboardSection()}"

if old_insights_render in content:
    content = content.replace(old_insights_render, new_insights_render)
    print("Removed standalone insights render!")
else:
    print("WARNING: Could not find standalone insights render")

# 3. Inject InsightsDashboard INSIDE LeaderboardSection, at the bottom (before closing </div>)
# The closing of LeaderboardSection ends with:
#     </div>
#     );
#   };
old_leaderboard_end = """    </div>
    );
  };

  const RankingsSection"""

new_leaderboard_end = """      <div style={{ marginTop: 24 }}>
        <InsightsDashboard data={data} overview={overview} topRanked={topRanked} bottomRanked={bottomRanked} centreBoard={centreBoard} selectedTestKey={selectedTestKey} />
      </div>
    </div>
    );
  };

  const RankingsSection"""

if old_leaderboard_end in content:
    content = content.replace(old_leaderboard_end, new_leaderboard_end)
    print("Injected InsightsDashboard into LeaderboardSection!")
else:
    print("WARNING: Could not find LeaderboardSection closing tag")

with open(filepath, 'w') as f:
    f.write(content)

print("Done! Insights now inside Centre Leaderboard tab.")
