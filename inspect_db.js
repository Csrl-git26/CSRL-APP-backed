const mongoose = require('mongoose');
const Profile = require('./models/Profile'); // Adjust path if needed
require('dotenv').config();

async function run() {
  await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/csrl', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });

  const students = await Profile.find({ 'tests.NCT01': { $exists: true } }).lean();
  console.log(`Found ${students.length} students with NCT01 test.`);
  
  let mbbsCount = 0;
  const mbbsStudents = [];
  
  for (const student of students) {
    const testData = student.tests.NCT01;
    // Check keys inside NCT01
    const hasMbbs = Object.keys(testData).some(key => key.toUpperCase().endsWith('MBBS'));
    if (hasMbbs) {
      mbbsCount++;
      mbbsStudents.push(student.name || student.enrollmentNumber);
    }
  }
  console.log(`Found ${mbbsCount} students with MBBS flag in NCT01.`);
  if (mbbsStudents.length > 0) {
    console.log('Sample MBBS students:', mbbsStudents.slice(0, 5));
    const sample = students.find(s => mbbsStudents.includes(s.name || s.enrollmentNumber));
    console.log('Sample NCT01 data:', JSON.stringify(sample.tests.NCT01, null, 2));
  } else {
    const sample = students[0];
    if (sample) console.log('Sample non-MBBS NCT01 data:', JSON.stringify(sample.tests.NCT01, null, 2));
  }

  mongoose.connection.close();
}

run().catch(console.error);
