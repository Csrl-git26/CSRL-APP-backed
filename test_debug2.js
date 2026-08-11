import './bootstrap-env.js';
import { isMongoReady, initMongo } from './services/mongoInit.js';
import { loadApplicationData, sliceCenterFromGlobal } from './services/dbService.js';
import { parseTestColumn } from './utils/testColumns.js';
import mongoose from 'mongoose';

async function run() {
  await initMongo();
  const global = await loadApplicationData();
  const source = sliceCenterFromGlobal(global, 'JDH');
  
  const testName = 'FMT08';
  console.log("Looking for testName:", testName);
  
  const matches = source.testColumns.filter(c => parseTestColumn(c).testName === testName);
  console.log("Matched columns:", matches.map(c => ({ col: c, parsed: parseTestColumn(c) })));
  
  process.exit(0);
}
run();
