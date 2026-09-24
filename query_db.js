const mongoose = require('mongoose');
const Profile = require('./models/Profile');
require('dotenv').config();

mongoose.connect(process.env.MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(async () => {
    console.log('Connected to MongoDB');
    // Find a profile that has tests.NCT01
    const profile = await Profile.findOne({ "tests.NCT01": { $exists: true } });
    console.log(JSON.stringify(profile.tests.NCT01, null, 2));
    
    // Find a profile that has tests.NCT01 and MBBS flag
    const mbbsProfile = await Profile.findOne({ "tests.NCT01.MBBS": { $exists: true } });
    if (mbbsProfile) {
        console.log("Found profile with tests.NCT01.MBBS:", mbbsProfile.studentId);
    } else {
        console.log("No profile with tests.NCT01.MBBS found.");
    }
    
    // Check for tests.NCT01.Mbbs
    const mbbsProfile2 = await Profile.findOne({ "tests.NCT01.Mbbs": { $exists: true } });
    if (mbbsProfile2) {
        console.log("Found profile with tests.NCT01.Mbbs:", mbbsProfile2.studentId);
    } else {
        console.log("No profile with tests.NCT01.Mbbs found.");
    }

    mongoose.disconnect();
  })
  .catch(err => console.error(err));
