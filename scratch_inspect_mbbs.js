const mongoose = require('mongoose');
const dotenv = require('dotenv');
dotenv.config();

const Profile = require('./models/Profile'); // Assuming models/Profile.js

async function check() {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    const profiles = await Profile.find({ 'tests.NCT01': { $exists: true } });
    let totalNct01 = profiles.length;
    let mbbsCount = 0;
    let mbbsVariants = {};
    let streams = {};
    
    profiles.forEach(p => {
      const test = p.tests.NCT01;
      let hasMbbs = false;
      let mbbsVal = null;
      
      for (const key of Object.keys(test)) {
         if (key.toUpperCase().includes('MBBS')) {
             hasMbbs = true;
             mbbsVal = test[key];
             mbbsVariants[key] = (mbbsVariants[key] || 0) + 1;
         }
      }
      
      if (hasMbbs && typeof mbbsVal === 'string' && mbbsVal.toUpperCase() === 'MBBS') {
          mbbsCount++;
          const stream = p.stream || 'not_set';
          streams[stream] = (streams[stream] || 0) + 1;
      }
    });

    console.log(`Total profiles with NCT01: ${totalNct01}`);
    console.log(`Total profiles with an MBBS flag (value 'MBBS') in NCT01: ${mbbsCount}`);
    console.log(`Variants of MBBS key found:`, mbbsVariants);
    console.log(`Streams of these MBBS students:`, streams);
  } catch (err) {
    console.error(err);
  } finally {
    process.exit();
  }
}
check();
