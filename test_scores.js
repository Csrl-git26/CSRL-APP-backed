import './bootstrap-env.js';
import { isMongoReady, initMongo } from './services/mongoInit.js';
import { loadApplicationData, sliceCenterFromGlobal } from './services/dbService.js';
import mongoose from 'mongoose';

async function run() {
  await initMongo();
  const global = await loadApplicationData();
  const source = sliceCenterFromGlobal(global, 'JDH');
  
  const fmt08 = source.tests.map(t => ({ roll: t.ROLL_KEY, total: t['FMT08'] }));
  console.log("FMT08 Totals:", fmt08);
  
  const avg = fmt08.reduce((sum, s) => sum + (parseFloat(s.total) || 0), 0) / fmt08.filter(s => s.total).length;
  console.log("FMT08 Average Total:", avg);
  
  process.exit(0);
}
run();
