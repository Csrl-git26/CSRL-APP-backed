const { connectDB } = require('./config/db');
const Profile = require('./models/Profile');
const TestScore = require('./models/TestScore');
async function run() {
  await connectDB();
  const centerCode = "CENTRE";
  const profiles = await Profile.find({ centerCode: { $regex: new RegExp(`^${centerCode}$`, 'i') } }).lean();
  console.log(`Found ${profiles.length} profiles for centre: ${centerCode}`);
  
  const rollKeys = profiles.map(p => p.ROLL_KEY);
  console.log(`Roll keys:`, rollKeys);
  
  const tests = await TestScore.find({ ROLL_KEY: { $in: rollKeys } }).lean();
  console.log(`Found ${tests.length} test scores for these profiles`);
  
  if (tests.length > 0) {
     console.log("Tests available:", Object.keys(tests[0].tests || {}));
  }
  process.exit();
}
run();
