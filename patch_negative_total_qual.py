import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestRecordsTable.jsx'
try:
    with open(filepath, 'r') as f:
        content = f.read()

    old_logic = "if (tot > 0 || total === 0) {"
    new_logic = "if (typeof tot === 'number') {"
    
    if old_logic in content:
        content = content.replace(old_logic, new_logic)
        with open(filepath, 'w') as f:
            f.write(content)
        print("Patched TestRecordsTable.jsx to support negative totals successfully!")
    else:
        print("Could not find the target logic in TestRecordsTable.jsx")
except Exception as e:
    print(f"Error patching file: {e}")
