import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Remove the sound hooks and logic
# Find the start of the component and the end of the sound logic
start_pattern = r"export default function CentreLeaderboard\(\{ centreStats = \[\], selTest, selectedSubject, onCentreClick \}\) \{"
end_pattern = r"  if \(\!selTest\) return <Empty message=\"Select a test to view rankings\" \/>;"

match = re.search(f"({start_pattern}).*?({end_pattern})", content, flags=re.DOTALL)
if match:
    new_start = match.group(1) + "\n" + match.group(2)
    content = content[:match.start()] + new_start + content[match.end():]
    print("Removed sound logic from component start!")
else:
    print("WARNING: Could not find sound logic block to remove")

# 2. Remove onMouseEnter from the SVG g
old_g = "<g style={{ pointerEvents: 'all', cursor: 'pointer' }} onMouseEnter={playAlertSound}>"
new_g = "<g style={{ pointerEvents: 'none' }}>"

if old_g in content:
    content = content.replace(old_g, new_g)
    print("Removed hover sound from SVG group!")
else:
    print("WARNING: Could not find onMouseEnter on SVG group")

# 3. Clean up imports
old_import = "import React, { useEffect, useRef, useCallback } from 'react';"
new_import = "import React from 'react';"
if old_import in content:
    content = content.replace(old_import, new_import)
    print("Cleaned up React imports!")
else:
    print("WARNING: Could not find React import to clean up")

with open(filepath, 'w') as f:
    f.write(content)

print("Done! Sound effect removed from CentreLeaderboard.")
