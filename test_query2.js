import mongoose from 'mongoose';
import dotenv from 'dotenv';
dotenv.config();

const ProfileSchema = new mongoose.Schema({}, { strict: false });
const Profile = mongoose.models.Profile || mongoose.model('Profile', ProfileSchema);

mongoose.connect(process.env.MONGODB_URI || "mongodb+srv://admin:YtL8ZtOaJ2sA8E6@csrl-app.2e1i8.mongodb.net/csrl_db?retryWrites=true&w=majority");

async function run() {
  const docs = await Profile.find({ ROLL_KEY: { $in: [2601035, '2601035'] } }).lean();
  console.log("Found", docs.length, "docs for 2601035");
  if (docs.length > 0) {
    console.log("Center:", docs[0].centerCode || docs[0].centreCode);
    console.log("Name:", docs[0]["STUDENT'S NAME"]);
  }
  process.exit();
}
run();
