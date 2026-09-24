import re

server_path = '/Users/surya/Desktop/CSRL-APP-backed/server.js'
with open(server_path, 'r') as f:
    server_content = f.read()

test_insights_logic = """
app.get('/api/analytics/test-insights', authenticateToken, async (req, res) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  const { testKey, rollKey, stream, centerCode } = req.query;
  if (!testKey) return res.status(400).json({ message: 'testKey is required' });

  let resolvedCenterCode = centerCode;
  if (!resolvedCenterCode || resolvedCenterCode === 'undefined' || resolvedCenterCode === 'null') {
    if (req.user.role === 'centre') {
      resolvedCenterCode = req.user.id;
    } else {
      resolvedCenterCode = '';
    }
  }

  const global = resolvedCenterCode ? await loadCenterApplicationData(resolvedCenterCode) : await loadApplicationData();
"""

old_pattern = r"app\.get\('/api/analytics/test-insights', authenticateToken, async \(req, res\) => \{\n  res\.setHeader\('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate'\);\n  res\.setHeader\('Pragma', 'no-cache'\);\n  res\.setHeader\('Expires', '0'\);\n  const \{ testKey, rollKey, stream \} = req\.query;\n  if \(!testKey\) return res\.status\(400\)\.json\(\{ message: 'testKey is required' \}\);\n\n  const global = await loadApplicationData\(\);"

server_content = re.sub(old_pattern, test_insights_logic.strip(), server_content)

with open(server_path, 'w') as f:
    f.write(server_content)
