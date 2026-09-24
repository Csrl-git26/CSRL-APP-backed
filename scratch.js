const mongoose = require('mongoose');
const Profile = require('./models/Profile'); // Adjust path if needed
require('dotenv').config(); // Ensure DB URI is loaded

async function run() {
  await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/csrl'); // Replace with actual DB if different
  
  const profiles = await Profile.find({});
  let totalNct01 = 0;
  let mbbsCount = 0;
  let mbbsCountWithStreamMatch = 0;
  
  for (const p of profiles) {
    if (p.tests && p.tests['NCT01']) {
      totalNct01++;
      const test = p.tests['NCT01'];
      const hasMbbsFlag = 
        (test.MBBS && test.MBBS.toString().toLowerCase() === 'mbbs') || 
        (test.Mbbs && test.Mbbs.toString().toLowerCase() === 'mbbs') ||
        (test.mbbs && test.mbbs.toString().toLowerCase() === 'mbbs');
        
      if (hasMbbsFlag) {
        mbbsCount++;
        // check how filterByStream might see them
        const stream = p.stream ? p.stream.toUpperCase() : '';
        const isNeetByStream = stream === 'NEET';
        const hasNeetTests = Object.keys(p.tests).some(k => k.startsWith('NCT') || k.startsWith('MMT') || k.startsWith('NMT'));
        if (isNeetByStream || hasNeetTests) {
            mbbsCountWithStreamMatch++;
        }
      }
    }
  }
  
  console.log(`Total Profiles with NCT01: ${totalNct01}`);
  console.log(`Profiles with MBBS flag in NCT01: ${mbbsCount}`);
  console.log(`Profiles with MBBS flag + NEET stream detected: ${mbbsCountWithStreamMatch}`);
  
  // Print a sample to see exactly how keys are formatted
  const sample = await Profile.findOne({ 'tests.NCT01.MBBS': { $exists: true } });
  if (sample) {
      console.log('Sample tests object with uppercase MBBS:', JSON.stringify(sample.tests.NCT01, null, 2));
  } else {
      const sample2 = await Profile.findOne({ 'tests.NCT01.Mbbs': { $exists: true } });
      if (sample2) console.log('Sample tests object with Mbbs:', JSON.stringify(sample2.tests.NCT01, null, 2));
  }
  
  process.exit();
}
run();
