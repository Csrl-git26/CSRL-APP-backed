import os

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

injection = """
  // Sync selectedTestKey to streamTestOptions
  useEffect(() => {
    if (streamTestOptions && streamTestOptions.length > 0 && selectedTestKey && !streamTestOptions.includes(selectedTestKey)) {
      const fallback = streamTestOptions.filter(o => o !== 'ALL_FMT')[0] || streamTestOptions[0];
      if (fallback) setSelectedTestKey(fallback);
    }
  }, [streamTestOptions, selectedTestKey]);

  // Sync selectedTestKey to leaderboard default
  useEffect(() => {
"""

content = content.replace("  // Sync selectedTestKey to leaderboard default\n  useEffect(() => {", injection)

with open(filepath, 'w') as f:
    f.write(content)

print("Injected selectedTestKey sync logic successfully.")
