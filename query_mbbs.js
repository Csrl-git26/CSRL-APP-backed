const mongoose = require('mongoose');
mongoose.connect('mongodb+srv://csrluser:csrllogin2024@csrl-backend.6m649.mongodb.net/?retryWrites=true&w=majority&appName=csrl-backend');
const TestScoreSchema = new mongoose.Schema({}, { strict: false });
const TestScore = mongoose.model('TestScore', TestScoreSchema);

async function run() {
  const docs = await TestScore.find({ "tests.NCT01": { $exists: true } }).lean();
  let count = 0;
  let vals = {};
  for (const doc of docs) {
     const mbbs = doc.tests.NCT01.MBBS || doc.tests.NCT01.Mbbs || doc.tests.NCT01.mbbs;
     if (mbbs) {
         vals[mbbs] = (vals[mbbs] || 0) + 1;
         if (String(mbbs).toUpperCase() === 'MBBS') count++;
     }
  }
  console.log("Total MBBS:", count);
  console.log("Values map:", vals);
  process.exit(0);
}
run();
