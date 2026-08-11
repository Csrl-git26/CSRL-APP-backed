import './bootstrap-env.js';
import { isMongoReady, initMongo } from './services/mongoInit.js';
import { loadApplicationData, sliceCenterFromGlobal } from './services/dbService.js';
import { parseTestColumn } from './utils/testColumns.js';
import mongoose from 'mongoose';

async function run() {
  await initMongo();
  const global = await loadApplicationData();
  const source = sliceCenterFromGlobal(global, 'JDH');
  
  const fmt08Cols = source.testColumns.filter(c => parseTestColumn(c).testName === 'FMT08');
  console.log("FMT08 Columns:", fmt08Cols);
  
  const totalCols = fmt08Cols.filter(c => parseTestColumn(c).isTotal || parseTestColumn(c).subject === 'Total');
  console.log("FMT08 Total Columns:", totalCols);
  
  process.exit(0);
}
run();
