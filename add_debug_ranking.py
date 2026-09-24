import re

server_path = '/Users/surya/Desktop/CSRL-APP-backed/server.js'
with open(server_path, 'r') as f:
    content = f.read()

debug_endpoint = """
app.get('/api/debug-ranking-nct01', async (req, res) => {
  try {
    const { loadApplicationData } = require('./services/dbService.js');
    const { rankStudentsByTest } = require('./services/analyticsService.js');
    const global = await loadApplicationData();
    const neetTests = global.tests.filter(t => Object.keys(t.tests || {}).some(k => k.startsWith('NCT')));
    
    const sample = neetTests.slice(0, 5);
    
    res.json({
      totalNeetTests: neetTests.length,
      sampleTests: sample,
      ranking: rankStudentsByTest(global.profiles, global.tests, 'NCT01')
    });
  } catch (err) {
    res.status(500).json({ error: err.message, stack: err.stack });
  }
});
"""

if '/api/debug-ranking-nct01' not in content:
    content = content.replace('app.listen(', debug_endpoint + '\napp.listen(')
    with open(server_path, 'w') as f:
        f.write(content)
    print("Debug endpoint added.")
else:
    print("Debug endpoint already exists.")
