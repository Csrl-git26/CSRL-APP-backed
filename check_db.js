import 'dotenv/config';
import { initMongo } from './services/dbService.js';
import TestScore from './models/TestScore.js';
import Profile from './models/Profile.js';

async function check() {
  await initMongo();
  const profileCount = await Profile.countDocuments();
  const testCount = await TestScore.countDocuments();
  console.log(`Profiles: ${profileCount}, Tests: ${testCount}`);
  process.exit(0);
}
check();
