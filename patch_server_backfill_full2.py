import re

filepath = '/Users/surya/Desktop/CSRL-APP-backed/server.js'
with open(filepath, 'r') as f:
    content = f.read()

old_block_start = content.find("// ── Temporary Migration Endpoint")
old_block_end = content.find("// ── Past Year Data Management")

content = content[:old_block_start] + """// ── Temporary Migration Endpoint ────────────────────────────────────────────────
app.post('/api/admin/backfill-test-topics', async (req, res) => {
  try {
    const { computeWeakTopics } = await import('./services/weakTopicService.js');
    const StudentRawMarks = (await import('./models/StudentRawMarks.js')).default;

    await initMongo();
    
    // 1. Find all unique testIds that have raw marks
    const distinctTests = await StudentRawMarks.distinct('testId');
    console.log(`[Backfill] Found ${distinctTests.length} tests to recompute.`);

    for (const testId of distinctTests) {
      console.log(`[Backfill] Recomputing testId: ${testId}`);
      await computeWeakTopics(testId);
    }
    
    return res.json({ success: true, message: 'Backfill complete. Recomputed ' + distinctTests.length + ' tests.' });
  } catch (e) {
    console.error(e);
    return res.status(500).json({ success: false, message: e.message });
  }
});

""" + content[old_block_end:]

with open(filepath, 'w') as f:
    f.write(content)
print("Updated migration endpoint")
