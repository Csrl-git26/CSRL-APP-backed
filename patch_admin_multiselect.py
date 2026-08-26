import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """            <MultiSelectDropdown 
              options={allTestOptions} 
              selectedOptions={selectedLeaderboardTestKeys} 
              onChange={setSelectedLeaderboardTestKeys} 
            />"""

new_block = """            <MultiSelectDropdown 
              options={allTestOptions.filter(o => o !== 'ALL_FMT')} 
              selectedOptions={selectedLeaderboardTestKeys} 
              onChange={setSelectedLeaderboardTestKeys} 
            />"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched AdminDashboard MultiSelectDropdown successfully!")
else:
    print("Could not find old_block in AdminDashboard.jsx")
