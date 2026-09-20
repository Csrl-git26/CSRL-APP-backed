const mongoose = require('mongoose');

const MONGO_URI = 'mongodb+srv://admin:YtL8ZtOaJ2sA8E6@csrl-app.2e1i8.mongodb.net/csrl_db?retryWrites=true&w=majority';

async function main() {
  await mongoose.connect(MONGO_URI);
  console.log('Connected to MongoDB');
  
  const db = mongoose.connection.db;
  
  // Check CenterOverallWeakTopics collection
  const overallDocs = await db.collection('centeroverallweaktopics').find({}, { projection: { centerId: 1, _id: 0 } }).toArray();
  console.log('\nCenterOverallWeakTopics centerIds:', overallDocs.map(d => d.centerId));
  
  // Check StudentRawMarks distinct centerIds
  const rawCenterIds = await db.collection('studentrawmarks').distinct('centerId');
  console.log('\nStudentRawMarks centerIds:', rawCenterIds);
  
  // Check CenterWeakTopics (per-test)
  const perTestDocs = await db.collection('centerweaktopics').distinct('centerId');
  console.log('\nCenterWeakTopics (per-test) centerIds:', perTestDocs);

  await mongoose.disconnect();
}

main().catch(e => { console.error(e); process.exit(1); });
