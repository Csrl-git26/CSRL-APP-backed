import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_end = """            </div>
          </>
        );
      })()}"""

new_end = """            </div>
          );
      })()}"""

content = content.replace(old_end, new_end)

with open(filepath, 'w') as f:
    f.write(content)

print("Fixed closing tags")
