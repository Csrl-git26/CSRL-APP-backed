require('dotenv').config();
const mongoose = require('mongoose');
const { StudentRawMarks } = require('./models/StudentRawMarks'); // adjust path if needed

async function run() {
  await mongoose.connect(process.env.MONGO_URI || 'mongodb://localhost:27017/csrl', { useNewUrlParser: true });
  const docs = await StudentRawMarks.find({}).limit(5).lean();
  if (docs.length === 0) {
    console.log("No StudentRawMarks found!");
  } else {
    console.log("Found some StudentRawMarks!");
    console.log("centerId of first doc:", docs[0].centerId);
    console.log("testId of first doc:", docs[0].testId);
  }
  process.exit(0);
}
run();
