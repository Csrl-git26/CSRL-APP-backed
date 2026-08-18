const mongoose = require('mongoose');

async function main() {
  await mongoose.connect('mongodb+srv://surya:qIqg2X2a537fK63s@csrl.6dhyi.mongodb.net/csrl_db?retryWrites=true&w=majority');
  const db = mongoose.connection;
  const Profile = db.collection('profiles');
  const TestScore = db.collection('testscores');

  const profiles = await Profile.find({ centerCode: 'ONGC-AGR' }).toArray();
  const rollKeys = profiles.map(p => p.ROLL_KEY || p.rollKey);

  const tests = await TestScore.find({ ROLL_KEY: { $in: rollKeys } }).toArray();

  const accTotals = {};
  const accCounts = {};
  const markTotals = {};

  tests.forEach(t => {
    if (t.tests && t.tests.FMT06) {
      for (const [subject, val] of Object.entries(t.tests.FMT06)) {
        if (subject.includes('_Accuracy')) {
          const subName = subject.replace('_Accuracy', '');
          const mark = parseFloat(val);
          if (!isNaN(mark)) {
            accTotals[subName] = (accTotals[subName] || 0) + mark;
            accCounts[subName] = (accCounts[subName] || 0) + 1;
          }
        } else if (!subject.includes('_')) { // Math, Physics
          const mark = parseFloat(val);
          if (!isNaN(mark)) {
            markTotals[subject] = (markTotals[subject] || 0) + mark;
          }
        }
      }
    }
  });

  console.log("AVERAGES FOR ONGC-AGR (FMT06):");
  for (const sub of Object.keys(markTotals)) {
    const accAvg = accCounts[sub] ? (accTotals[sub] / accCounts[sub]).toFixed(1) : 'N/A';
    const markAvg = accCounts[sub] ? (markTotals[sub] / accCounts[sub]).toFixed(1) : 'N/A';
    console.log(`${sub}: Mark Avg = ${markAvg}, Acc Avg = ${accAvg}% (Count: ${accCounts[sub]})`);
  }

  process.exit(0);
}

main().catch(console.error);
