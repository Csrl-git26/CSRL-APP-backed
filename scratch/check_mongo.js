const mongoose = require('mongoose');

async function main() {
  await mongoose.connect('mongodb://localhost:27017/csrl', { // Assuming local DB
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });

  const profiles = await mongoose.connection.collection('profiles').find({
    $or: [
      { 'tests.NCT01_MBBS': { $exists: true } },
      { 'tests.NCT01_Mbbs': { $exists: true } },
      { 'tests.NCT01.Mbbs': { $exists: true } },
      { 'tests.NCT01.MBBS': { $exists: true } }
    ]
  }).limit(5).toArray();

  console.log("Found profiles:", profiles.length);
  if (profiles.length > 0) {
     profiles.forEach(p => {
         console.log(`ID: ${p._id}, Stream: ${p.stream}`);
         console.log(JSON.stringify(p.tests, null, 2));
     });
  }

  // Count MBBS specific
  const countNew = await mongoose.connection.collection('profiles').countDocuments({ 'tests.NCT01_MBBS': { $regex: /^mbbs$/i } });
  const countOld1 = await mongoose.connection.collection('profiles').countDocuments({ 'tests.NCT01_Mbbs': { $regex: /^mbbs$/i } });
  const countOld2 = await mongoose.connection.collection('profiles').countDocuments({ 'tests.NCT01.Mbbs': { $regex: /^mbbs$/i } });
  
  console.log(`Count tests.NCT01_MBBS: ${countNew}`);
  console.log(`Count tests.NCT01_Mbbs: ${countOld1}`);
  console.log(`Count tests.NCT01.Mbbs: ${countOld2}`);

  await mongoose.disconnect();
}

main().catch(console.error);
