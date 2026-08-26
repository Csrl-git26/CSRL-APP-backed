import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestRecordsTable.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_logic = """                  if (tot >= overallMin && p >= 20 && c >= 20 && m >= 20) {
                    isQualified = true;
                  }"""

new_logic = """                  if (tot >= overallMin) {
                    isQualified = true;
                  }"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched TestRecordsTable.jsx successfully!")
else:
    print("Could not find the old logic block in TestRecordsTable.jsx")

