const mongoose = require('mongoose');
const Profile = require('./models/Profile'); // Adjust path if needed
require('dotenv').config();

async function run() {
  await mongoose.connect(process.env.MONGO_URI || 'mongodb://localhost:27017/csrl', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });

  const allProfiles = await Profile.find({});
  console.log(`Total profiles: ${allProfiles.length}`);

  let nct01MbbsCount = 0;
  let nct01MbbsCountCaseInsensitive = 0;
  
  for (const p of allProfiles) {
    if (p.tests && p.tests.NCT01) {
       // Check new format NCT01_MBBS
       if (p.tests.NCT01_MBBS) {
           console.log(`Found NCT01_MBBS on ${p.studentName}: ${p.tests.NCT01_MBBS}`);
           if (String(p.tests.NCT01_MBBS).toUpperCase() === 'MBBS') nct01MbbsCount++;
       }
       // Check old format tests.NCT01.MBBS
       if (p.tests.NCT01.MBBS || p.tests.NCT01.Mbbs || p.tests.NCT01.mbbs) {
           nct01MbbsCountCaseInsensitive++;
       }
    } else if (p.tests && p.tests.NCT01_MBBS) {
       // Wait, flatToNested puts it at root of tests?
       if (String(p.tests.NCT01_MBBS).toUpperCase() === 'MBBS') {
           nct01MbbsCount++;
       }
    }
  }

  // Let's just find anything with 'mbbs' in its tests object for NCT01
  let totalMbbs = 0;
  let withNCT01 = 0;
  allProfiles.forEach(p => {
      let hasMbbs = false;
      let hasNCT01 = false;
      if (!p.tests) return;
      
      const testKeys = Object.keys(p.tests);
      if (testKeys.some(k => k.startsWith('NCT01'))) hasNCT01 = true;
      if (hasNCT01) withNCT01++;

      // Check all keys in tests object
      for (const key of Object.keys(p.tests)) {
          if (key.includes('NCT01') && key.toUpperCase().includes('MBBS')) {
              if (String(p.tests[key]).toUpperCase() === 'MBBS') hasMbbs = true;
          }
          if (typeof p.tests[key] === 'object') {
              for (const subKey of Object.keys(p.tests[key])) {
                  if (subKey.toUpperCase().includes('MBBS') && String(p.tests[key][subKey]).toUpperCase() === 'MBBS') {
                      hasMbbs = true;
                  }
              }
          }
      }
      if (hasMbbs) totalMbbs++;
  });

  console.log(`Profiles with NCT01 tests: ${withNCT01}`);
  console.log(`Total students with MBBS for NCT01: ${totalMbbs}`);

  process.exit();
}

run();
