import mongoose from 'mongoose';
import dotenv from 'dotenv';
dotenv.config();

const uri = process.env.MONGODB_URI || process.env.MONGO_URI;

mongoose.connect(uri)
  .then(async () => {
    const TestScore = (await import('./models/TestScore.js')).default;
    const mbbsCount = await TestScore.countDocuments({
      $or: [
        { "tests.NCT01.MBBS": { $exists: true } },
        { "tests.NCT01.Mbbs": { $exists: true } },
        { "tests.NCT01.mbbs": { $exists: true } }
      ]
    });
    console.log("Current NCT01 MBBS Count in MongoDB:", mbbsCount);
    process.exit(0);
  })
  .catch(err => {
    console.error(err);
    process.exit(1);
  });
