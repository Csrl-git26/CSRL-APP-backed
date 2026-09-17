import { initMongo } from './services/mongoInit.js';
import { loadApplicationData } from './services/dbService.js';
import { computeTestInsights } from './services/analyticsService.js';
import mongoose from 'mongoose';

async function run() {
  await initMongo();
  const global = await loadApplicationData();
  const res = computeTestInsights(global.profiles, global.tests, 'MMT01', global.testColumns, { stream: 'NEET' });
  console.log(res.subjectTopStudents.map(s => s.subject));
  console.log(res.globalSubjectStats.map(s => s.subject));
  mongoose.disconnect();
}
run();
