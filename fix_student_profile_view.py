import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad = """      </>
      )}
      </>
      )}
      {/* HIDDEN PRINTABLE CONTAINER */}"""

good = """      </>
      )}
      {/* HIDDEN PRINTABLE CONTAINER */}"""

if bad in content:
    content = content.replace(bad, good)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Fixed syntax error in StudentProfileView.")
else:
    print("Could not find duplicated tags.")

