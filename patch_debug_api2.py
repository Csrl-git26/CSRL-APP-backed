import re

with open('server.js', 'r') as f:
    content = f.read()

if "app.get('/api/debug/student'" not in content:
    debug_endpoint = """
app.get('/api/debug/student/:roll', async (req, res) => {
  const { roll } = req.params;
  const { Profile, TestScore } = require('./services/dbService.js');
  // wait, dbService doesn't export models, let me just read all global data
  const global = await loadApplicationData();
  const p = global.profiles.find(x => String(x.ROLL_KEY) === String(roll));
  const t = global.tests.find(x => String(x.ROLL_KEY) === String(roll));
  res.json({ profile: p, test: t, profileCenterCode: p?.centerCode, testCenter: t?.Center });
});
"""
    content = content.replace("app.get('/api/health'", debug_endpoint + "\napp.get('/api/health'")

    with open('server.js', 'w') as f:
        f.write(content)
    print("Debug endpoint added")
else:
    print("Debug endpoint already exists")
