import mongoose from 'mongoose';
import dotenv from 'dotenv';
import { loadApplicationData } from './services/dbService.js';

dotenv.config();

async function run() {
  const data = await loadApplicationData();
  const cmt01Cols = data.testColumns.filter(c => c.startsWith('CMT01_') || c.startsWith('MMT01_'));
  console.log('Columns found:', cmt01Cols);
  process.exit(0);
}

run();
