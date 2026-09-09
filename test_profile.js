import mongoose from 'mongoose';
import dotenv from 'dotenv';
dotenv.config();

const ProfileSchema = new mongoose.Schema({}, { strict: false });
const Profile = mongoose.models.Profile || mongoose.model('Profile', ProfileSchema);
const TestScoreSchema = new mongoose.Schema({}, { strict: false });
const TestScore = mongoose.models.TestScore || mongoose.model('TestScore', TestScoreSchema);

mongoose.connect(process.env.MONGODB_URI || "mongodb+srv://admin:YtL8ZtOaJ2sA8E6@csrl-app.2e1i8.mongodb.net/csrl_db?retryWrites=true&w=majority");

async function run() {
  const profile = await Profile.findOne({ ROLL_KEY: { $in: [2618003, '2618003'] } }).lean();
  console.log("Profile for 2618003:", profile ? "EXISTS" : "MISSING");
  
  const test = await TestScore.findOne({ ROLL_KEY: { $in: [2618003, '2618003'] } }).lean();
  console.log("Test for 2618003:", test ? "EXISTS" : "MISSING");

  const profile2 = await Profile.findOne({ ROLL_KEY: { $in: [2601035, '2601035'] } }).lean();
  console.log("Profile for 2601035:", profile2 ? "EXISTS" : "MISSING");
  
  process.exit();
}
run();
