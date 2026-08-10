const mongoose = require('mongoose');

async function main() {
  await mongoose.connect('mongodb+srv://surya:qIqg2X2a537fK63s@csrl.6dhyi.mongodb.net/csrl_db?retryWrites=true&w=majority');
  const db = mongoose.connection;
  
  const StudentWeakTopics = db.collection('studentweaktopics');
  const ApplicationData = db.collection('applicationdatas');

  const weakTopics = await StudentWeakTopics.find({ studentId: '2601001' }).toArray();
  const global = await ApplicationData.findOne({});
  const testDoc = global.tests.find((t) => t.ROLL_KEY === '2601001') || {};
  
  console.log("TEST COLUMNS:");
  console.log(global.testColumns.filter(c => c.includes('FMT')));
  
  console.log("WEAK TOPICS:");
  for (const wt of weakTopics) {
    if (wt.testId.includes('FMT')) {
      console.log(JSON.stringify(wt, null, 2));
    }
  }

  process.exit(0);
}

main().catch(console.error);
