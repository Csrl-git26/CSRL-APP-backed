const mongoose = require('mongoose');

mongoose.connect('mongodb://127.0.0.1:27017/csrl_db', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(async () => {
  console.log('Connected to DB');
  const db = mongoose.connection.db;
  
  const profiles = await db.collection('profiles').find({
    $or: [
      { 'tests.NCT01_MBBS': { $exists: true } },
      { 'tests.NCT01_Mbbs': { $exists: true } }
    ]
  }).toArray();
  
  console.log(`Total profiles with NCT01 MBBS flags: ${profiles.length}`);
  let countMBBS = 0;
  let countMbbs = 0;
  profiles.forEach(p => {
    if (p.tests.NCT01_MBBS) countMBBS++;
    if (p.tests.NCT01_Mbbs) countMbbs++;
  });
  console.log(`With NCT01_MBBS: ${countMBBS}`);
  console.log(`With NCT01_Mbbs: ${countMbbs}`);
  
  process.exit(0);
})
.catch(err => {
  console.error(err);
  process.exit(1);
});
