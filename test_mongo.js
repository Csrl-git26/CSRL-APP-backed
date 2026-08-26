import mongoose from 'mongoose';
import dotenv from 'dotenv';
import StudentRawMarks from './models/StudentRawMarks.js';

dotenv.config({ path: '.env.local' });
if (!process.env.MONGO_URI) {
  const fs = require('fs');
  const envFile = fs.readFileSync('.env', 'utf8');
  const match = envFile.match(/MONGO_URI=(.*)/);
  if (match) process.env.MONGO_URI = match[1].trim();
}

mongoose.connect("mongodb+srv://developer:12345@cluster0.aigtd.mongodb.net/csrl_db?retryWrites=true&w=majority")
  .then(async () => {
    const docs = await StudentRawMarks.find().limit(1).lean();
    console.log(JSON.stringify(docs, null, 2));
    process.exit();
  })
  .catch(console.error);
