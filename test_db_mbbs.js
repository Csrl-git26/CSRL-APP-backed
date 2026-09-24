const mongoose = require('mongoose');
const Profile = require('./models/Profile'); // Adjust path if needed
require('dotenv').config();

async function checkMBBS() {
  try {
    await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/csrl', {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    
    console.log("Connected to DB");
    
    // Find profiles with NCT01 data
    const profiles = await Profile.find({ 'tests.NCT01': { $exists: true } });
    console.log(`Found ${profiles.length} profiles with NCT01 data.`);
    
    let mbbsCount = 0;
    let oldMbbsCount = 0;
    let nct01Count = 0;

    profiles.forEach(p => {
      const nct01 = p.tests.NCT01;
      if (nct01) {
        nct01Count++;
        if (nct01.MBBS && String(nct01.MBBS).toLowerCase() === 'mbbs') {
            mbbsCount++;
        }
        if (nct01.Mbbs && String(nct01.Mbbs).toLowerCase() === 'mbbs') {
            oldMbbsCount++;
        }
      }
    });

    console.log(`Total NCT01 records: ${nct01Count}`);
    console.log(`Records with NCT01.MBBS = 'MBBS': ${mbbsCount}`);
    console.log(`Records with NCT01.Mbbs = 'MBBS': ${oldMbbsCount}`);
    
  } catch (err) {
    console.error(err);
  } finally {
    mongoose.disconnect();
  }
}

checkMBBS();
