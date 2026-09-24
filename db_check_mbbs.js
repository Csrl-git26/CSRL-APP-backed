const mongoose = require('mongoose');
const Profile = require('./models/Profile'); // Adjust path if needed
require('dotenv').config();

async function checkData() {
  await mongoose.connect(process.env.MONGO_URI || 'mongodb://localhost:27017/csrl', { useNewUrlParser: true, useUnifiedTopology: true });
  console.log("Connected to DB");
  
  // Find profiles with NCT01 data
  const profiles = await Profile.find({ 'tests.NCT01': { $exists: true } }).lean();
  console.log(`Total profiles with NCT01 data: ${profiles.length}`);
  
  let mbbsCount = 0;
  let mbbsCasedCount = 0;
  let nestedMBBSCount = 0;
  let nestedMbbsCount = 0;
  
  profiles.forEach(p => {
    const test = p.tests.NCT01;
    if (test) {
      if (test.MBBS) nestedMBBSCount++;
      if (test.Mbbs) nestedMbbsCount++;
      if (test.NCT01_MBBS) mbbsCount++;
      if (test.NCT01_Mbbs) mbbsCasedCount++;
      
      // Print first one we find that has some MBBS flag for inspection
      if ((test.MBBS || test.Mbbs || test.NCT01_MBBS || test.NCT01_Mbbs) && (mbbsCount + mbbsCasedCount + nestedMBBSCount + nestedMbbsCount === 1)) {
         console.log("Sample test object:", test);
      }
    }
  });
  
  console.log({ mbbsCount, mbbsCasedCount, nestedMBBSCount, nestedMbbsCount });
  process.exit(0);
}
checkData().catch(console.error);
