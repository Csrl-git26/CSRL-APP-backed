import mongoose from 'mongoose';
import { isMongoReady, initMongo } from './services/mongoInit.js';
import StudentWeakTopics from './models/StudentWeakTopics.js';
import dotenv from 'dotenv';
dotenv.config();

async function run() {
  await initMongo();
  const docs = await StudentWeakTopics.find({ testId: { $in: ['FMT04', 'FMT 04', 'fmt04'] } }).limit(5);
  console.log(JSON.stringify(docs, null, 2));
  mongoose.disconnect();
}
run();
