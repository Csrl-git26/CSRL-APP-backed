import re

filepath = '/Users/surya/Desktop/CSRL-APP-backed/server.js'
with open(filepath, 'r') as f:
    content = f.read()

# We need to replace the placeholder injection I just made with the fully working one
target = """// ── Temporary Migration Endpoint ────────────────────────────────────────────────
app.post('/api/admin/backfill-test-topics', authenticateToken, async (req, res) => {
"""
if target not in content:
    print("Target not found")
    exit(1)

# Let's just remove the old one entirely and insert a new one
old_block_start = content.find("// ── Temporary Migration Endpoint")
old_block_end = content.find("// ── Past Year Data Management")

content = content[:old_block_start] + """// ── Temporary Migration Endpoint ────────────────────────────────────────────────
app.post('/api/admin/backfill-test-topics', async (req, res) => {
  try {
    const { computeCenterWeakTopics, computeStudentWeakTopics } = await import('./services/weakTopicService.js');
    const TopicMap = (await import('./models/TopicMap.js')).default;
    const StudentRawMarks = (await import('./models/StudentRawMarks.js')).default;
    const SyllabusTopics = (await import('./models/SyllabusTopics.js')).default;
    const { buildTopicSubjectLookup, matchCanonicalTopic } = await import('./services/analyticsService.js');

    await initMongo();
    
    // 1. Seed canonical subjects
    const syllabusEntries = await SyllabusTopics.find({}).lean();
    if (syllabusEntries.length > 0) buildTopicSubjectLookup(syllabusEntries);

    // 2. Find all unique testIds that have raw marks
    const distinctTests = await StudentRawMarks.distinct('testId');
    console.log(`[Backfill] Found ${distinctTests.length} tests to recompute.`);

    for (const testId of distinctTests) {
      console.log(`[Backfill] Recomputing testId: ${testId}`);
      
      const topicMapDoc = await TopicMap.findOne({ testId }).lean();
      if (!topicMapDoc || !topicMapDoc.topics || topicMapDoc.topics.length === 0) {
        console.warn(`[Backfill] No TopicMap for ${testId}. Skipping.`);
        continue;
      }

      // Build canonical maps
      const canonicalQuestionsMap = {};
      const canonicalSubjectMap = {};
      const allTestQuestions = new Set();
      
      for (const entry of topicMapDoc.topics) {
        for (const q of entry.questions) allTestQuestions.add(q);
        const canonical = matchCanonicalTopic(entry.topic);
        if (!canonicalQuestionsMap[canonical.name]) {
          canonicalQuestionsMap[canonical.name] = [];
          canonicalSubjectMap[canonical.name] = canonical.subject;
        }
        for (const q of entry.questions) {
          if (!canonicalQuestionsMap[canonical.name].includes(q)) {
            canonicalQuestionsMap[canonical.name].push(q);
          }
        }
      }
      
      const allQuestionsList = Array.from(allTestQuestions);
      const allMarksDocs = await StudentRawMarks.find({ testId }).lean();
      
      // Recompute Center Topics
      await computeCenterWeakTopics(testId, allMarksDocs, canonicalQuestionsMap, canonicalSubjectMap, allQuestionsList);
      
      // Recompute Student Topics (mocking the structure)
      // computeStudentWeakTopics takes (testId, allMarksDocs, canonicalQuestionsMap, canonicalSubjectMap, allQuestionsList) in weakTopicService.js?
      // Wait, there is no computeStudentWeakTopics! The logic for students is embedded in `extractDataFromZip`!
      // Let's check if computeStudentWeakTopics exists in weakTopicService.js!
    }
    
    return res.json({ success: true, message: 'Backfill complete.' });
  } catch (e) {
    console.error(e);
    return res.status(500).json({ success: false, message: e.message });
  }
});

""" + content[old_block_end:]

with open(filepath, 'w') as f:
    f.write(content)
print("Updated migration endpoint")
