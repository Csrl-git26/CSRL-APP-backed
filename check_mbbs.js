require('dotenv').config();
const mongoose = require('mongoose');
const Profile = require('./models/Profile'); // Adjust path if needed

async function check() {
  await mongoose.connect(process.env.MONGODB_URI);
  const profiles = await Profile.find({ "tests.NCT01": { $exists: true } });
  
  let mbbsCount = 0;
  let mbbsStudents = [];
  
  for (const p of profiles) {
    const test = p.tests.NCT01;
    if (test && (test.MBBS || test.Mbbs || test.mbbs)) {
      mbbsCount++;
      mbbsStudents.push({ 
        name: p.name, 
        center: p.center, 
        stream: p.stream,
        nct01: test
      });
    }
  }
  
  console.log(`Total profiles with NCT01: ${profiles.length}`);
  console.log(`Total with MBBS flag: ${mbbsCount}`);
  if (mbbsCount > 0) {
      console.log("Sample of 5 MBBS students:");
      console.log(JSON.stringify(mbbsStudents.slice(0, 5), null, 2));
  }
  
  // also check if any are getting filtered by center
  
  await mongoose.disconnect();
}
check().catch(console.error);
