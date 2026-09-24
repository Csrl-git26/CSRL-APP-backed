const mongoose = require('mongoose');
require('dotenv').config();
async function run() {
  await mongoose.connect(process.env.MONGODB_URI || 'mongodb+srv://developer:a5F0g1w0f1Yv74u3@cluster0.o98z0.mongodb.net/csrl_db?retryWrites=true&w=majority&appName=Cluster0');
  const Test = mongoose.model('Test', new mongoose.Schema({}, { strict: false }));
  const docs = await Test.find({ 'NCT01_MBBS': { $exists: true } }).limit(5);
  console.log('Docs with NCT01_MBBS:', docs.map(d => ({ roll: d.ROLL_KEY, flag: d.NCT01_MBBS })));
  const count = await Test.countDocuments({ 'NCT01_MBBS': 'MBBS' });
  console.log('Count of MBBS = MBBS:', count);
  process.exit(0);
}
run();
