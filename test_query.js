import mongoose from 'mongoose';
import dotenv from 'dotenv';
import StudentRawMarks from './models/StudentRawMarks.js';

dotenv.config();
mongoose.connect(process.env.MONGO_URI);

async function run() {
  const docs = await StudentRawMarks.find({ studentId: '2601001' }).lean();
  console.log("Found", docs.length, "docs for 2601001");
  if (docs.length > 0) {
    console.log(docs[0]);
  }
  process.exit();
}
run();
