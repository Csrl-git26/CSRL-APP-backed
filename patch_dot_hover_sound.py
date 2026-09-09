filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Fix: outer g has pointerEvents:none; we need to enable events on the red dot inner <g>
# Change the outer g to keep none, but the inner red dot g gets pointer events + onMouseEnter
old_red_dot_g = """      <g style={{ pointerEvents: 'none' }}>
        {isRedFlag && (
          <g>"""

new_red_dot_g = """      <g style={{ pointerEvents: 'none' }}>
        {isRedFlag && (
          <g style={{ pointerEvents: 'all', cursor: 'pointer' }} onMouseEnter={playAlertSound}>"""

if old_red_dot_g in content:
    content = content.replace(old_red_dot_g, new_red_dot_g)
    print("Added onMouseEnter sound to red dot SVG group!")
else:
    print("WARNING: Could not find red dot <g> block")

with open(filepath, 'w') as f:
    f.write(content)

print("Done! Hover sound on red dot added.")
