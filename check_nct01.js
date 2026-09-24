require('dotenv').config();
const mongoose = require('mongoose');
const Profile = require('./models/Profile'); // Adjust path if necessary

mongoose.connect(process.env.MONGODB_URI)
  .then(async () => {
    console.log("Connected to MongoDB.");
    
    // Find documents that have NCT01 data
    const docs = await Profile.find({ "tests.NCT01": { $exists: true } }).limit(5).lean();
    console.log("Sample records with NCT01 tests:");
    docs.forEach(doc => {
      console.log(`RegNo: ${doc.regNo}, Name: ${doc.name}, Stream: ${doc.stream}`);
      console.log(`NCT01 keys:`, Object.keys(doc.tests.NCT01 || {}));
      console.log(`NCT01 data:`, doc.tests.NCT01);
    });

    const docsWithMbbs = await Profile.find({ 
      $or: [
        { "tests.NCT01_MBBS": { $exists: true } },
        { "tests.NCT01.MBBS": { $exists: true } },
        { "tests.NCT01.Mbbs": { $exists: true } },
        { "tests.NCT01.mbbs": { $exists: true } },
        { "tests.NCT01_Mbbs": { $exists: true } }
      ]
    }).limit(5).lean();

    console.log("\nSample records with any MBBS key for NCT01:");
    docsWithMbbs.forEach(doc => {
      console.log(`RegNo: ${doc.regNo}, Name: ${doc.name}`);
      console.log(`NCT01 data:`, doc.tests.NCT01);
      // check root keys just in case
      Object.keys(doc.tests).forEach(k => {
        if (k.includes('NCT01')) console.log(`Key ${k}:`, doc.tests[k]);
      });
    });

    mongoose.disconnect();
  })
  .catch(err => {
    console.error("Error:", err);
    process.exit(1);
  });
