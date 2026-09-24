import { loadApplicationData } from './services/dbService.js';
import { filterByStream } from './server.js';
import { computeTestInsights } from './services/analyticsService.js';
import { initMongo } from './services/mongoInit.js';

async function run() {
  await initMongo();
  const global = await loadApplicationData();
  
  // Mock what test-insights does for DDN/DEL MT01 JEE
  const { profiles, tests } = global;
  
  // Filter for DEL
  const delProfiles = profiles.filter(p => p.centerCode === 'DEL');
  const rollKeys = new Set(delProfiles.map(p => p.ROLL_KEY));
  const delTests = tests.filter(t => rollKeys.has(t.ROLL_KEY));
  
  // In server.js filterByStream is used, but we'll skip it for a moment to see if computeTestInsights works
  const result = computeTestInsights(delProfiles, delTests, "MT01", global.testColumns, { stream: 'JEE' });
  
  console.log("overallTopper:", result.overallTopper);
  console.log("rankedStudents length:", result.rankedStudents.length);
  if (result.rankedStudents.length > 0) {
      console.log("top 2 ranked:", result.rankedStudents.slice(0, 2));
  }
  
  process.exit(0);
}
run();
