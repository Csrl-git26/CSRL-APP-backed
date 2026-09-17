import { initMongo } from './services/mongoInit.js';
import { loadApplicationData } from './services/dbService.js';
import mongoose from 'mongoose';

async function run() {
  await initMongo();
  const global = await loadApplicationData();
  console.log("TEST COLUMNS:", global.testColumns);
  mongoose.disconnect();
}
run();
