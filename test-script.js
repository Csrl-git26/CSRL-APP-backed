import 'dotenv/config';
import { initMongo } from './services/mongoInit.js';
import StudentRawMarks from './models/StudentRawMarks.js';

async function run() {
  await initMongo();
  console.log("Connected to MongoDB");
  let rawDocs = await StudentRawMarks.find({ centerId: 'AGR' }).lean();
  console.log("rawDocs count for AGR:", rawDocs.length);
  if (rawDocs.length > 0) {
    const testIds = Array.from(new Set(rawDocs.map(d => d.testId)));
    console.log("testIds:", testIds);
  }
  process.exit(0);
}
run();
