import os

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad_block = """  // Sync selectedTestKey to streamTestOptions
  useEffect(() => {
    if (streamTestOptions && streamTestOptions.length > 0 && selectedTestKey && !streamTestOptions.includes(selectedTestKey)) {
      const fallback = streamTestOptions.filter(o => o !== 'ALL_FMT')[0] || streamTestOptions[0];
      if (fallback) setSelectedTestKey(fallback);
    }
  }, [streamTestOptions, selectedTestKey]);

"""

if bad_block in content:
    content = content.replace(bad_block, "")
    print("Removed bad block")
else:
    print("Could not find bad block!")

good_block = """
  // Sync selectedTestKey to streamTestOptions
  useEffect(() => {
    if (streamTestOptions && streamTestOptions.length > 0 && selectedTestKey && !streamTestOptions.includes(selectedTestKey)) {
      const fallback = streamTestOptions.filter(o => o !== 'ALL_FMT')[0] || streamTestOptions[0];
      if (fallback) setSelectedTestKey(fallback);
    }
  }, [streamTestOptions, selectedTestKey]);

  const activeLeaderboardKeys = useMemo(() => {"""

if "const activeLeaderboardKeys = useMemo(() => {" in content:
    content = content.replace("  const activeLeaderboardKeys = useMemo(() => {", good_block)
    print("Inserted good block")
else:
    print("Could not find insertion point!")

with open(filepath, 'w') as f:
    f.write(content)

print("Patching done!")
