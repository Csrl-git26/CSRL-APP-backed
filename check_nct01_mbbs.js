const mongoose = require('mongoose');
const Profile = require('./models/Profile'); // Adjust path if needed
require('dotenv').config();

async function check() {
  await mongoose.connect(process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/csrl', {
    useNewUrlParser: true,
    useUnifiedTopology: true
  });

  const allProfiles = await Profile.find({'tests.NCT01': { $exists: true }});
  console.log(`Total profiles with NCT01: ${allProfiles.length}`);
  
  let countMBBS = 0;
  let countMbbs = 0;
  let countmbbs = 0;
  let hasBoth = 0;

  let streamCounts = {};

  allProfiles.forEach(p => {
    const t = p.tests.NCT01;
    let found = false;
    if (t.MBBS) {
      countMBBS++;
      found = true;
    }
    if (t.Mbbs) {
      countMbbs++;
      found = true;
    }
    if (t.mbbs) {
      countmbbs++;
      found = true;
    }
    
    if (t.MBBS && t.Mbbs) {
      hasBoth++;
    }

    if (found) {
      const stream = p.stream || 'none';
      streamCounts[stream] = (streamCounts[stream] || 0) + 1;
    }
  });

  console.log(`count MBBS: ${countMBBS}`);
  console.log(`count Mbbs: ${countMbbs}`);
  console.log(`count mbbs: ${countmbbs}`);
  console.log(`Profiles with both MBBS and Mbbs: ${hasBoth}`);
  console.log(`Stream distribution for MBBS qualified:`, streamCounts);

  mongoose.disconnect();
}

check();
