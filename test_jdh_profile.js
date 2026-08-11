import './bootstrap-env.js';
import { isMongoReady, initMongo } from './services/mongoInit.js';
import { loadApplicationData, sliceCenterFromGlobal } from './services/dbService.js';
import mongoose from 'mongoose';

async function run() {
  await initMongo();
  const global = await loadApplicationData();
  const source = sliceCenterFromGlobal(global, 'JDH');
  
  if (source.profiles.length > 0) {
    console.log("First profile:", source.profiles[0]);
  }
  
  process.exit(0);
}
run();
