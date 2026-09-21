import mongoose from "mongoose";

let legacyIndexesDropped = false;

export const dropLegacyIndexes = async () => {
  if (legacyIndexesDropped) return;
  try {
    const db = mongoose.connection.db;
    if (!db) return;

    try {
      await db.collection('studentoverallweaktopics').dropIndex('studentId_1');
      console.log("✅ Dropped obsolete index studentId_1 from studentoverallweaktopics");
    } catch (e) {
      // index does not exist or already dropped
    }

    try {
      await db.collection('centeroverallweaktopics').dropIndex('centerId_1');
      console.log("✅ Dropped obsolete index centerId_1 from centeroverallweaktopics");
    } catch (e) {
      // index does not exist or already dropped
    }

    legacyIndexesDropped = true;
  } catch (err) {
    console.warn("⚠️ Note on dropping legacy indexes:", err.message);
  }
};

export const initMongo = async () => {
  try {
    if (mongoose.connection.readyState !== 1) {
      await mongoose.connect(process.env.MONGODB_URI);
      console.log("✅ MongoDB Connected");
    }
    await dropLegacyIndexes();

    try {
      console.log("RUNNING ONE-TIME CLEANUP FOR MBBS FLAGS...");
      const TestScore = (await import('../models/TestScore.js')).default;
      const res = await TestScore.updateMany({}, {
          $unset: {
              "tests.NCT01.MBBS": "",
              "tests.NCT01.Mbbs": "",
              "tests.NCT01.mbbs": "",
              "tests.NCT01.STATUS": "",
              "tests.NCT01.Status": "",
              "tests.NCT01.status": "",
              "NCT01_MBBS": "",
              "NCT01_Mbbs": "",
              "NCT01_mbbs": "",
              "NCT01_STATUS": "",
              "NCT01_Status": "",
              "NCT01_status": ""
          }
      });
      console.log(`CLEANUP SUCCESSFUL! Modified ${res.modifiedCount} documents.`);
    } catch (cleanupErr) {
      console.log("❌ Cleanup Error:", cleanupErr.message);
    }

  } catch (err) {
    console.log("❌ MongoDB Error:", err.message);
  }
};

export const isMongoReady = () => mongoose.connection.readyState === 1;