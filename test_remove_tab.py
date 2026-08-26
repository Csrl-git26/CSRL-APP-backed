import sys
filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()
if "{ key: 'leaderboard', Icon: Trophy,         label: 'Centre Leaderboard' }," in content:
    print("Found leaderboard tab in CentreDashboard")
