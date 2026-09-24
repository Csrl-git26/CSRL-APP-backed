require('dotenv').config();
const mongoose = require('mongoose');
const Profile = require('./models/Profile');

async function check() {
  await mongoose.connect(process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/csrl', { useNewUrlParser: true, useUnifiedTopology: true });
  
  // Find a student who has NCT01 tests
  const profiles = await Profile.find({ "tests.NCT01": { $exists: true } }).lean();
  console.log(`Found ${profiles.length} profiles with NCT01 data.`);
  
  let mbbsCount = 0;
  for (const p of profiles) {
    const t = p.tests.NCT01;
    if (t.MBBS === 'MBBS' || t.Mbbs === 'MBBS' || t.mbbs === 'MBBS') {
      mbbsCount++;
    } else if (t.MBBS === 'mbbs' || t.Mbbs === 'mbbs' || t.mbbs === 'mbbs') {
        mbbsCount++;
    } else if (Object.keys(t).some(k => k.toUpperCase() === 'MBBS' && String(t[k]).toUpperCase() === 'MBBS')) {
        mbbsCount++;
    }
  }
  
  console.log(`Manually counted MBBS students for NCT01: ${mbbsCount}`);
  
  // Let's print a sample profile's NCT01 data
  const sample = profiles.find(p => p.tests.NCT01 && Object.keys(p.tests.NCT01).some(k => k.toUpperCase() === 'MBBS' && String(p.tests.NCT01[k]).toUpperCase() === 'MBBS'));
  if (sample) {
      console.log("Sample Profile with MBBS:");
      console.log(JSON.stringify(sample.tests.NCT01, null, 2));
      console.log("Center:", sample.center);
      console.log("Stream:", sample.stream);
  } else {
      console.log("No profile found with MBBS flag in NCT01.");
      // Just print one of them
      if (profiles.length > 0) {
          console.log("Sample Profile (no MBBS flag):");
          console.log(JSON.stringify(profiles[0].tests.NCT01, null, 2));
      }
  }
  
  mongoose.disconnect();
}
check();
