import mongoose from 'mongoose';
import { Profile } from './models/DataModels.js';
import dotenv from 'dotenv';
dotenv.config();

async function run() {
  await mongoose.connect(process.env.MONGODB_URI);
  const total = await Profile.countDocuments();
  const centre = await Profile.countDocuments({ centerCode: /^centre$/i });
  console.log(`Total: ${total}, Centre: ${centre}`);
  process.exit(0);
}
run();
