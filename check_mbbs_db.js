import 'dotenv/config';
import mongoose from 'mongoose';
import { initMongo } from './services/dbService.js';
import TestScore from './models/TestScore.js';

async function check() {
  await initMongo();
  const docs = await TestScore.find({ 'tests.NCT01': { $exists: true } }).limit(5).lean();
  console.log("Looking at 5 random NCT01 records:");
  docs.forEach(d => {
    console.log(d.ROLL_KEY, Object.keys(d.tests.NCT01));
  });

  // check if any document has 'MBBS' case-insensitively in NCT01
  const allDocs = await TestScore.find({ 'tests.NCT01': { $exists: true } }).lean();
  let mbbsCount = 0;
  for (const doc of allDocs) {
    const keys = Object.keys(doc.tests.NCT01);
    if (keys.some(k => k.toUpperCase().includes('MBBS'))) {
      mbbsCount++;
      console.log(`Found MBBS flag in ${doc.ROLL_KEY}:`, keys.filter(k => k.toUpperCase().includes('MBBS')));
    }
  }
  console.log(`Total students with MBBS flag found in DB: ${mbbsCount}`);
  process.exit(0);
}
check();
