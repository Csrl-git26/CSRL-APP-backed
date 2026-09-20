const mongoose = require('mongoose');

const MONGO_URI = process.env.MONGO_URI || 'mongodb+srv://admin:YtL8ZtOaJ2sA8E6@csrl-app.2e1i8.mongodb.net/csrl_db?retryWrites=true&w=majority';

async function main() {
  await mongoose.connect(MONGO_URI);
  console.log('Connected to MongoDB');
  
  const db = mongoose.connection.db;
  const centerDoc = await db.collection('centeroverallweaktopics').findOne({ centerId: 'GAIL' });
  console.log('Center strong topics:', centerDoc?.subjectWise?.PHYSICS?.strong?.slice(0, 3));

  const studentDoc = await db.collection('studentoverallweaktopics').findOne();
  console.log('Student strong topics:', studentDoc?.subjectWise?.PHYSICS?.strong?.slice(0, 3));
  
  await mongoose.disconnect();
}

main().catch(e => { console.error(e); process.exit(1); });
