import 'dotenv/config';
import mongoose from 'mongoose';
import { initMongo } from './services/dbService.js';
import TestScore from './models/TestScore.js';

async function check() {
  await initMongo();
  const allDocs = await TestScore.find({ 'tests.NCT01': { $exists: true } }).lean();
  console.log(`Found ${allDocs.length} docs with NCT01`);
  if (allDocs.length > 0) {
     const sample = allDocs[0].tests.NCT01;
     console.log("Keys in NCT01 for first doc:", Object.keys(sample));
     console.log("Values for these keys:");
     for (let k of Object.keys(sample)) {
        console.log(`  ${k}: ${sample[k]}`);
     }
  }

  process.exit(0);
}
check();
