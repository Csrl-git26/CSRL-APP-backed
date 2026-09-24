import mongoose from 'mongoose';
import { TestScore } from './models/TestScore.js';

async function run() {
  await mongoose.connect(process.env.MONGODB_URI || 'mongodb+srv://csrluser:csrlpass123@cluster0.abcde.mongodb.net/csrl_db?retryWrites=true&w=majority', { useNewUrlParser: true, useUnifiedTopology: true });
  const docs = await TestScore.find({}).lean();
  const neet = docs.find(d => Object.keys(d).some(k => k.startsWith('NCT')));
  console.log("NEET DOC keys:", Object.keys(neet).filter(k => k.startsWith('NCT')));
  console.log("NCT01 values:", Object.keys(neet).filter(k => k.startsWith('NCT')).reduce((acc, k) => { acc[k] = neet[k]; return acc; }, {}));
  process.exit(0);
}
run();
