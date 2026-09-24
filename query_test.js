const mongoose = require('mongoose');
const Profile = require('./models/Profile'); // Adjust path as needed
require('dotenv').config();

mongoose.connect(process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/csrl', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
}).then(async () => {
  const profile = await Profile.findOne({ "tests.NCT01": { $exists: true } }).select('tests.NCT01').lean();
  console.log(JSON.stringify(profile, null, 2));
  
  const mbbsProfiles = await Profile.find({ "tests.NCT01_MBBS": { $exists: true } }).select('csrl_id tests').limit(2).lean();
  console.log("MBBS in flat root keys:", JSON.stringify(mbbsProfiles, null, 2));

  mongoose.connection.close();
});
