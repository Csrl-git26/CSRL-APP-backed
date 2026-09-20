import fetch from 'node-fetch';
import { loadApplicationData } from './services/dbService.js';
import { sliceCenterFromGlobal, buildCentreChartData } from './services/dbService.js';
import mongoose from 'mongoose';
import dotenv from 'dotenv';
dotenv.config();

async function run() {
  await mongoose.connect(process.env.MONGO_URI);
  const global = await loadApplicationData();
  const source = sliceCenterFromGlobal(global, "AGR");
  const finalChartData = buildCentreChartData(source.centerTests, source.testColumns);
  console.log("Excel Chart Data Length:", finalChartData.length);
  console.log(finalChartData.map(d => d.name));
  process.exit(0);
}
run();
