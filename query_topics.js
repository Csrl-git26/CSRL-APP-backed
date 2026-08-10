require('dotenv').config();
const mongoose = require('mongoose');

async function run() {
  await mongoose.connect(process.env.MONGO_URI);
  console.log("Connected");
  const CenterWeakTopics = mongoose.connection.collection('centerweaktopics');
  const docs = await CenterWeakTopics.find({ centerId: 'ABN' }).toArray();
  console.log(JSON.stringify(docs, null, 2));
  mongoose.disconnect();
}
run();
