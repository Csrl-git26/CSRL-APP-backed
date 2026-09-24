const mongoose = require('mongoose');
const Profile = require('./models/Profile'); // Adjust path if needed
require('dotenv').config();

async function check() {
  await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/csrl'); // adjust if different URI
  
  // Find all profiles that have some NCT01 data
  const profiles = await Profile.find({ 'tests.NCT01': { $exists: true } });
  
  let mbbsCount = 0;
  let hasMbbsKey = 0;
  let mbbsVals = [];

  for (let p of profiles) {
    let testData = p.tests.NCT01;
    // Check for MBBS flag
    const hasMbbs = testData.MBBS || testData.Mbbs || testData.mbbs;
    if (testData.MBBS) hasMbbsKey++;
    if (hasMbbs && String(hasMbbs).trim().toUpperCase() === 'MBBS') {
        mbbsCount++;
    } else if (hasMbbs) {
        mbbsVals.push(hasMbbs);
    }
  }

  console.log(`Total profiles with NCT01: ${profiles.length}`);
  console.log(`Profiles with MBBS key: ${hasMbbsKey}`);
  console.log(`Profiles with MBBS value 'MBBS': ${mbbsCount}`);
  console.log(`Other MBBS values: ${mbbsVals.slice(0, 10).join(', ')}`);

  process.exit(0);
}
check();
