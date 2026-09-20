filepath = "/Users/surya/Desktop/CSRL-APP-frontend/src/services/dataService.js"
with open(filepath, "r") as f:
    content = f.read()

old = """export function buildStudentChartData(studentTests, testColumns) {
  const testsMap = {};

  (testColumns || []).forEach((col) => {"""

new = """export function buildStudentChartData(studentTests, testColumns) {
  const testsMap = {};

  // Filter out cross-stream tests (e.g. NEET tests for JEE students)
  const studentStream = ((studentTests && studentTests.stream) || 'JEE').toUpperCase();
  const NEET_TEST_PREFIX = /^(MMT|NCT|NMT|NEET)/i;
  const relevantColumns = (testColumns || []).filter((col) => {
    const { testName } = parseTestColumn(col);
    const isNeetTest = NEET_TEST_PREFIX.test(testName);
    if (studentStream === 'NEET') return true;
    return !isNeetTest;
  });

  relevantColumns.forEach((col) => {"""

if old in content:
    content = content.replace(old, new)
    with open(filepath, "w") as f:
        f.write(content)
    print("Patched frontend buildStudentChartData with stream filter")
else:
    print("ERROR: Target string not found. Check spacing.")
