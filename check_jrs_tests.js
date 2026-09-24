import mongoose from 'mongoose';
import dotenv from 'dotenv';
dotenv.config();

mongoose.connect(process.env.MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(async () => {
    console.log('Connected to MongoDB');
    const TestScore = (await import('./models/TestScore.js')).default;
    
    const count = await TestScore.countDocuments();
    console.log(`Total TestScores in DB: ${count}`);
    
    const jrsTezTests = await TestScore.find({
      $or: [
        { centerCode: { $in: ['JRS', 'TEZ'] } },
        { ROLL_KEY: { $regex: 'JRS|TEZ', $options: 'i' } }
      ]
    }).lean();
    
    console.log(`Found ${jrsTezTests.length} tests for JRS or TEZ.`);
    
    if (jrsTezTests.length > 0) {
      console.log('Sample test:', JSON.stringify(jrsTezTests[0], null, 2));
    }
    
    process.exit(0);
  })
  .catch(err => {
    console.error(err);
    process.exit(1);
  });
