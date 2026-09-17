import mongoose from 'mongoose';

async function run() {
  try {
    await mongoose.connect('mongodb+srv://admin:YtL8ZtOaJ2sA8E6@csrl-app.2e1i8.mongodb.net/csrl_db?retryWrites=true&w=majority');
    const db = mongoose.connection.db;
    const doc = await db.collection('centerweaktopics').findOne({ testId: 'CMT01' });
    console.log(JSON.stringify(doc, null, 2));
    process.exit(0);
  } catch(e) {
    console.error(e);
    process.exit(1);
  }
}
run();
