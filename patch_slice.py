filepath = '../CSRL-APP-backed/services/dbService.js'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """  const testColumns = colSet.size > 0 ? Array.from(colSet) : globalData.testColumns;
  return { profiles, tests, testColumns };"""

new_block = """  // Always return all global test columns so the Centre Dashboard can see 
  // all available tests in the dropdown (like NCT01) even if their students haven't taken them.
  const testColumns = globalData.testColumns;
  return { profiles, tests, testColumns };"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Successfully patched sliceCenterFromGlobal")
else:
    print("Could not find block in sliceCenterFromGlobal")
