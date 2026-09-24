require('dotenv').config();
const mongoose = require('mongoose');
const Profile = require('./models/Profile');

async function run() {
  try {
    await mongoose.connect(process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/csrl');
    console.log("Connected to MongoDB.");

    const profiles = await Profile.find({ 
      $or: [
        { "tests.NCT01": { $exists: true } },
        { "tests.NCT01_MBBS": { $exists: true } },
        { "tests.NCT01_Mbbs": { $exists: true } }
      ]
    }).lean();

    console.log(`Total records with NCT01 data: ${profiles.length}`);
    
    let mbbsCount = 0;
    profiles.forEach(p => {
      const t = p.tests || {};
      let hasMBBS = false;
      if (t.NCT01 && (t.NCT01.MBBS || t.NCT01.Mbbs || t.NCT01.mbbs)) hasMBBS = true;
      if (t.NCT01_MBBS || t.NCT01_Mbbs || t.NCT01_mbbs) hasMBBS = true;
      
      if (hasMBBS) mbbsCount++;
    });

    console.log(`Total records with MBBS flag for NCT01: ${mbbsCount}`);
    
    if (profiles.length > 0) {
      console.log("Sample test object for first profile:");
      console.log(JSON.stringify(profiles[0].tests, null, 2));
    }

    process.exit(0);
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
}
run();
