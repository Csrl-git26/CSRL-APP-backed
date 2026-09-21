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
      
      // TEMPORARY CLEANUP SCRIPT (Will run once on deployment)
      setTimeout(async () => {
          try {
              console.log("RUNNING TEMPORARY CLEANUP SCRIPT FOR MMT01, MMT02, AND NCT01 MBBS...");
              const TestScore = (await import('../models/TestScore.js')).default;
              const res = await TestScore.updateMany({}, {
                  $unset: {
                      "tests.MMT01": "",
                      "tests.MMT02": "",
                      "tests.NCT01.MBBS": "",
                      "tests.NCT01.Mbbs": "",
                      "tests.NCT01.mbbs": ""
                  }
              });
              console.log(`CLEANUP SUCCESSFUL! Modified ${res.modifiedCount} documents.`);
          } catch(e) {
              console.error("Cleanup script failed:", e);
          }
      }, 10000);
    }
    await dropLegacyIndexes();
  } catch (err) {
    console.log("❌ MongoDB Error:", err.message);
  }
};

export const isMongoReady = () => mongoose.connection.readyState === 1;