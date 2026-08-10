import mongoose from 'mongoose';
import dotenv from 'dotenv';
dotenv.config();

const uri = process.env.MONGODB_URI;

const StudentRawMarksSchema = new mongoose.Schema({
  studentId: String,
  testId: String,
  marks: Map,
}, { strict: false });

const RawMarks = mongoose.model('StudentRawMarks', StudentRawMarksSchema, 'studentrawmarks');

async function run() {
  await mongoose.connect(uri);
  const doc = await RawMarks.findOne({ studentId: '2601001', testId: 'FMT 04' }).lean();
  if (doc) {
    console.log("Marks for FMT 04:");
    for (const [q, m] of Object.entries(doc.marks)) {
      console.log(q, ":", m);
    }
  } else {
    console.log("No doc found");
  }
  process.exit(0);
}
run();
