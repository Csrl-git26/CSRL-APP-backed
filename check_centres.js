import { initMongo } from './services/mongoInit.js';
import TestScore from './models/TestScore.js';
import StudentRawMarks from './models/StudentRawMarks.js';

async function check() {
  await initMongo();
  
  const allTests = await TestScore.find({}).lean();
  console.log(`Total tests: ${allTests.length}`);
  
  const jrsTests = allTests.filter(t => t.ROLL_KEY && t.ROLL_KEY.includes('JRS'));
  const tezTests = allTests.filter(t => t.ROLL_KEY && t.ROLL_KEY.includes('TEZ'));
  
  console.log(`JRS tests: ${jrsTests.length}`);
  console.log(`TEZ tests: ${tezTests.length}`);
  
  if (jrsTests.length > 0) {
      console.log('JRS Sample keys:', Object.keys(jrsTests[0]));
  }
  
  process.exit(0);
}

check();
