const mongoose = require('mongoose');
const dotenv = require('dotenv');
dotenv.config();

mongoose.connect(process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/csrl_db')
  .then(async () => {
    const Profile = require('./models/Profile');
    const profiles = await Profile.find({ "tests.NCT01": { $exists: true } }).lean();
    
    let totalNCT01 = profiles.length;
    let mbbsCount = 0;
    let keyCounts = {};
    let vals = {};

    profiles.forEach(p => {
      const t = p.tests.NCT01;
      let foundMbbs = false;
      for (let k in t) {
        if (k.toLowerCase().includes('mbbs')) {
          keyCounts[k] = (keyCounts[k] || 0) + 1;
          const valStr = String(t[k]);
          vals[valStr] = (vals[valStr] || 0) + 1;
          if (valStr.toUpperCase() === 'MBBS') {
             foundMbbs = true;
          }
        }
      }
      if (foundMbbs) mbbsCount++;
    });

    console.log(`Total NCT01 records: ${totalNCT01}`);
    console.log(`MBBS Count (case-insensitive value 'MBBS'): ${mbbsCount}`);
    console.log(`Keys found:`, keyCounts);
    console.log(`Values found:`, vals);
    process.exit(0);
  })
  .catch(err => {
    console.error(err);
    process.exit(1);
  });
