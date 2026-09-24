import { initMongo } from './services/mongoInit.js';
import TestScore from './models/TestScore.js';

async function run() {
  await initMongo();
  
  // Find all docs that have tests.ALL
  const docs = await TestScore.find({ 'tests.ALL': { $exists: true } }).lean();
  console.log(`Found ${docs.length} docs with tests.ALL`);
  
  if (docs.length > 0) {
    const result = await TestScore.updateMany(
      { 'tests.ALL': { $exists: true } },
      { $unset: { 'tests.ALL': '' } }
    );
    console.log(`Cleaned ${result.modifiedCount} documents`);
  }
  
  process.exit(0);
}
run();
