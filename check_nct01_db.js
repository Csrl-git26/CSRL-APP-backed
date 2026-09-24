const mongoose = require('mongoose');
const dotenv = require('dotenv');
dotenv.config();

// Connect to the database
mongoose.connect(process.env.MONGO_URI || process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/csrl_db', {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(async () => {
  console.log("Connected to MongoDB successfully.");
  
  try {
    const Profile = require('./models/Profile');

    // Count different variations of the NCT01 MBBS key that might exist
    const c1 = await Profile.countDocuments({ 'tests.NCT01_MBBS': { $regex: /^mbbs$/i } });
    const c2 = await Profile.countDocuments({ 'tests.NCT01.MBBS': { $regex: /^mbbs$/i } });
    const c3 = await Profile.countDocuments({ 'tests.NCT01.Mbbs': { $regex: /^mbbs$/i } });

    console.log(`Profiles with tests.NCT01_MBBS (new flat format): ${c1}`);
    console.log(`Profiles with tests.NCT01.MBBS (nested upper): ${c2}`);
    console.log(`Profiles with tests.NCT01.Mbbs (nested old): ${c3}`);

    // Total that have the flag in any form
    const totalWithFlag = await Profile.countDocuments({
      $or: [
        { 'tests.NCT01_MBBS': { $regex: /^mbbs$/i } },
        { 'tests.NCT01.MBBS': { $regex: /^mbbs$/i } },
        { 'tests.NCT01.Mbbs': { $regex: /^mbbs$/i } }
      ]
    });
    console.log(`Total unique profiles with some NCT01 MBBS flag: ${totalWithFlag}`);

  } catch (err) {
    console.error("Error querying:", err);
  } finally {
    mongoose.disconnect();
  }
}).catch(err => {
  console.error("Database connection error:", err);
});
