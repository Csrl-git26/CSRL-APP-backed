const mongoose = require('mongoose');
const Profile = require('./models/Profile'); // Adjust path if needed
require('dotenv').config();

mongoose.connect(process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/csrl', { useNewUrlParser: true, useUnifiedTopology: true })
  .then(async () => {
    console.log("Connected to MongoDB");
    
    // Find one profile with NCT01 test
    const sample = await Profile.findOne({ 'tests.NCT01': { $exists: true } });
    if (sample) {
      console.log("Sample Profile keys for tests.NCT01:", Object.keys(sample.tests.NCT01 || {}));
      console.log("Sample tests keys:", Object.keys(sample.tests || {}));
      console.log("NCT01 object:", sample.tests.NCT01);
    }
    
    const countMbbsNested = await Profile.countDocuments({ 'tests.NCT01.MBBS': { $regex: /^mbbs$/i } });
    const countMbbsFlat = await Profile.countDocuments({ 'tests.NCT01_MBBS': { $regex: /^mbbs$/i } });
    const countMbbsOther = await Profile.countDocuments({ 'tests.NCT01.Mbbs': { $regex: /^mbbs$/i } });
    
    console.log("Count tests.NCT01.MBBS:", countMbbsNested);
    console.log("Count tests.NCT01_MBBS:", countMbbsFlat);
    console.log("Count tests.NCT01.Mbbs:", countMbbsOther);

    mongoose.disconnect();
  })
  .catch(err => {
    console.error(err);
    process.exit(1);
  });
