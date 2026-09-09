import mongoose from 'mongoose';
import dotenv from 'dotenv';
dotenv.config();

const ProfileSchema = new mongoose.Schema({}, { strict: false });
const Profile = mongoose.models.Profile || mongoose.model('Profile', ProfileSchema);
const TestScoreSchema = new mongoose.Schema({}, { strict: false });
const TestScore = mongoose.models.TestScore || mongoose.model('TestScore', TestScoreSchema);

mongoose.connect(process.env.MONGODB_URI || "mongodb+srv://admin:YtL8ZtOaJ2sA8E6@csrl-app.2e1i8.mongodb.net/csrl_db?retryWrites=true&w=majority");

async function run() {
  const normCenter = 'AGR';
  const allTests = await TestScore.find({}).lean();
  
  function ensureNested(d) {
    if (d.tests) return d;
    const { _id, ROLL_KEY, centerCode, ...tests } = d;
    return { _id, ROLL_KEY, centerCode, tests };
  }

  const relevantRollKeys = new Set();
  const tDocs = allTests.filter(d => {
    const raw = { ...d };
    const nested = ensureNested(raw);
    let belongsToCenter = false;
    
    if (nested.centerCode && String(nested.centerCode).trim().toLowerCase() === normCenter.toLowerCase()) {
      belongsToCenter = true;
    }
    
    for (const t of Object.values(nested.tests || {})) {
      if (t.centerCode && String(t.centerCode).trim().toLowerCase() === normCenter.toLowerCase()) {
        belongsToCenter = true;
        break;
      }
    }
    
    if (belongsToCenter && nested.ROLL_KEY) {
      relevantRollKeys.add(String(nested.ROLL_KEY));
      return true;
    }
    return false;
  });

  console.log("Total tests matched for AGR:", tDocs.length);
  console.log("Is 2601095 in relevantRollKeys?", relevantRollKeys.has('2601095'));

  const profilesDocs = await Profile.find({
    $or: [
      { centerCode: new RegExp('^AGR$', 'i') },
      { ROLL_KEY: { $in: Array.from(relevantRollKeys) } }
    ]
  }).lean();
  
  console.log("Total profiles found for AGR:", profilesDocs.length);
  const foundProfile = profilesDocs.find(p => String(p.ROLL_KEY) === '2601095');
  console.log("Found profile for 2601095 in DB query?", !!foundProfile);
  if (!foundProfile) {
      // Let's check if the profile exists AT ALL
      const rawProfile = await Profile.findOne({ ROLL_KEY: '2601095' }).lean();
      console.log("Does profile 2601095 exist AT ALL?", !!rawProfile);
      if (rawProfile) console.log("Its center code is:", rawProfile.centerCode || rawProfile.centreCode);
  }

  process.exit();
}
run();
