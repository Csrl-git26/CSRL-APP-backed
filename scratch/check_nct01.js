const mongoose = require('mongoose');
require('dotenv').config();

mongoose.connect(process.env.MONGO_URI || 'mongodb://localhost:27017/csrl', {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(async () => {
  const Profile = require('./models/Profile');

  // Find all profiles that have some kind of MBBS flag for NCT01
  const allProfiles = await Profile.find({ "tests.NCT01": { $exists: true } });
  
  let mbbsCount = 0;
  let mbbsKeys = new Set();

  allProfiles.forEach(p => {
    const nct01 = p.tests.NCT01;
    let hasMbbs = false;
    for (const key of Object.keys(nct01)) {
      if (key.toUpperCase().includes('MBBS')) {
        hasMbbs = true;
        mbbsKeys.add(key);
      }
    }
    if (hasMbbs) {
      mbbsCount++;
    }
  });

  console.log(`Total students with NCT01: ${allProfiles.length}`);
  console.log(`Total students with MBBS flag in NCT01: ${mbbsCount}`);
  console.log(`MBBS keys found:`, Array.from(mbbsKeys));

  mongoose.connection.close();
});
