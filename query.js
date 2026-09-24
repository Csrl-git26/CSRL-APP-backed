const mongoose = require('mongoose');
const Profile = require('./models/Profile'); // Adjust path if needed
require('dotenv').config();

mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/csrl', {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(async () => {
  console.log("Connected to MongoDB");
  
  // Find a few profiles with NCT01 tests
  const profiles = await Profile.find({ "tests.NCT01": { $exists: true } }).limit(5).lean();
  
  for (const p of profiles) {
    console.log(`CSRL ID: ${p.csrl_id}`);
    console.log(JSON.stringify(p.tests.NCT01, null, 2));
    console.log("Stream:", p.stream);
  }
  
  // Count how many have NCT01_MBBS or something similar
  const mbbsCount = await Profile.countDocuments({
    $or: [
      { "tests.NCT01.Mbbs": { $exists: true } },
      { "tests.NCT01.MBBS": { $exists: true } },
      { "tests.NCT01.mbbs": { $exists: true } },
      { "tests.NCT01_MBBS": { $exists: true } }
    ]
  });
  console.log("Total docs with some NCT01 MBBS flag:", mbbsCount);
  
  mongoose.connection.close();
}).catch(err => {
  console.error(err);
  process.exit(1);
});
