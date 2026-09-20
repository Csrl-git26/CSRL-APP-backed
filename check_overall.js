import mongoose from 'mongoose';
import { initMongo } from './services/mongoInit.js';
import CenterOverallWeakTopics from './models/CenterOverallWeakTopics.js';

async function run() {
  await initMongo();
  const docs = await CenterOverallWeakTopics.find().lean();
  console.log("Found CenterOverallWeakTopics docs:", docs.length);
  if (docs.length > 0) {
    console.log("Sample:", docs[0].centerId, docs[0].testsIncluded);
  }
  process.exit(0);
}
run();
