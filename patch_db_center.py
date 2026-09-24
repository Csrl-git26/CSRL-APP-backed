filepath = '../CSRL-APP-backed/services/dbService.js'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """  const profileRollKeys = profilesDocs.map(p => String(p.ROLL_KEY));
  const finalTestDocs = allTests.filter(d => {
    const raw = { ...d };
    const nested = ensureNested(raw);
    return relevantRollKeys.has(String(nested.ROLL_KEY)) || profileRollKeys.includes(String(nested.ROLL_KEY));
  });

  return processDbDocuments(profilesDocs, finalTestDocs);
}"""

new_block = """  const profileRollKeys = profilesDocs.map(p => String(p.ROLL_KEY));
  const finalTestDocs = allTests.filter(d => {
    const raw = { ...d };
    const nested = ensureNested(raw);
    return relevantRollKeys.has(String(nested.ROLL_KEY)) || profileRollKeys.includes(String(nested.ROLL_KEY));
  });

  const result = processDbDocuments(profilesDocs, finalTestDocs);
  
  // Extract test columns from ALL tests globally, not just this centre's tests.
  // This ensures the Centre Dashboard can see all available tests in the dropdown (like NCT01),
  // even if this specific centre hasn't uploaded scores for it yet.
  const allTestColumnsSet = new Set();
  allTests.forEach(d => {
    const raw = { ...d };
    delete raw._id; delete raw.__v; delete raw.createdAt; delete raw.updatedAt;
    const nested = ensureNested(raw);
    extractColumnsFromNestedTests(nested.tests).forEach(c => allTestColumnsSet.add(c));
  });
  result.testColumns = Array.from(allTestColumnsSet);
  
  return result;
}"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Successfully patched loadCenterDataFromDb to return all global test columns")
else:
    print("Could not find the block in dbService.js")
