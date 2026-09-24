require('dotenv').config();
const mongoose = require('mongoose');

async function check() {
  await mongoose.connect(process.env.MONGODB_URI);
  const db = mongoose.connection.db;
  const Profile = db.collection('profiles');
  
  const total = await Profile.countDocuments();
  console.log(`Total profiles: ${total}`);
  
  const mbbs_nct01 = await Profile.countDocuments({ "tests.NCT01_MBBS": "MBBS" });
  console.log(`Profiles with tests.NCT01_MBBS = 'MBBS': ${mbbs_nct01}`);
  
  const mbbs_nct01_case = await Profile.countDocuments({ "tests.NCT01_MBBS": { $regex: /^mbbs$/i } });
  console.log(`Profiles with tests.NCT01_MBBS regex: ${mbbs_nct01_case}`);

  const mbbs_any = await Profile.countDocuments({ "tests.NCT01.Mbbs": { $exists: true } });
  console.log(`Profiles with tests.NCT01.Mbbs exists: ${mbbs_any}`);

  const mbbs_any_case = await Profile.countDocuments({ "tests.NCT01.MBBS": { $exists: true } });
  console.log(`Profiles with tests.NCT01.MBBS exists: ${mbbs_any_case}`);

  const sample = await Profile.findOne({ "tests.NCT01": { $exists: true } }, { projection: { tests: 1, csr_id: 1, _id: 0 } });
  console.log("Sample Profile with NCT01:", JSON.stringify(sample, null, 2));
  
  mongoose.disconnect();
}
check();
