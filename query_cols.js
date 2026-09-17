import mongoose from 'mongoose';
import dotenv from 'dotenv';
import { loadGlobalDataFromDb } from './services/dbService.js';

dotenv.config();

async function run() {
  const data = await loadGlobalDataFromDb();
  console.log(data.testColumns);
  process.exit(0);
}

run();
