import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    old_block = """  const LeaderboardSection = () => {
    const totalAppeared = centreBoard.reduce((sum, c) => sum + (c.tested || 0), 0);
    const totalQualified = centreBoard.reduce((sum, c) => sum + (c.qualifiedCount || 0), 0);
    const qualPct = totalAppeared > 0 ? Math.round((totalQualified / totalAppeared) * 100) : 0;"""

    new_block = """  const LeaderboardSection = () => {
    let testCount = selectedLeaderboardTestKeys.length;
    if (testCount === 1 && selectedLeaderboardTestKeys[0] === 'ALL_FMT') {
      testCount = allTestOptions.filter(o => String(o).startsWith('FMT') && o !== 'ALL_FMT').length;
    }
    const numTests = Math.max(1, testCount);
    
    const totalAppeared = Math.round(centreBoard.reduce((sum, c) => sum + (c.tested || 0), 0) / numTests);
    const totalQualifiedRaw = centreBoard.reduce((sum, c) => sum + (c.qualifiedCount || 0), 0);
    const totalQualified = Math.round(totalQualifiedRaw / numTests);
    const qualPct = totalAppeared > 0 ? Math.round((totalQualified / totalAppeared) * 100) : 0;"""

    if old_block in content:
        content = content.replace(old_block, new_block)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Patched {filepath} successfully!")
    else:
        print(f"Could not find old_block in {filepath}")

patch_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx')
patch_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx')
