import fs
import re

server_path = '/Users/surya/Desktop/CSRL-APP-backed/server.js'
with open(server_path, 'r') as f:
    content = f.read()

debug_endpoint = """
app.get('/api/debug-glt-nct01', async (req, res) => {
  try {
    const { TestScore, Profile } = require('./services/dbService.js');
    const tests = await TestScore.find({}).lean();
    let nct_tests = tests.filter(d => Object.keys(d.tests || {}).some(k => k.startsWith('NCT')));
    let glt_tests = nct_tests.filter(d => {
       const nested = d.tests || {};
       if (d.centerCode === 'GLT') return true;
       for (const k of Object.keys(nested)) {
           if (nested[k].centerCode === 'GLT') return true;
       }
       return false;
    });
    const profiles = await Profile.find({ centerCode: 'GLT' }).lean();
    res.json({
      total_nct_tests: nct_tests.length,
      glt_nct_tests: glt_tests.length,
      glt_nct_tests_data: glt_tests,
      glt_profiles: profiles.length
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});
"""

if '/api/debug-glt-nct01' not in content:
    # Insert before app.listen or at the end
    content = content.replace('app.listen(', debug_endpoint + '\napp.listen(')
    with open(server_path, 'w') as f:
        f.write(content)
    print("Debug endpoint added.")
else:
    print("Debug endpoint already exists.")
