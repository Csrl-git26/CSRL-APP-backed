const mongoose = require('mongoose');
require('dotenv').config();
const Profile = require('./models/Profile');

async function checkDB() {
    try {
        await mongoose.connect(process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/csrl');
        console.log("Connected to DB.");

        const students = await Profile.find({ "tests.NCT01": { $exists: true } }).lean();
        console.log(`Total students with NCT01 data: ${students.length}`);

        let mbbsCount = 0;
        let sample = null;

        for (const s of students) {
            const t = s.tests.NCT01;
            if (t && (t.MBBS || t.Mbbs || t.mbbs || t._MBBS)) {
                mbbsCount++;
                if (!sample) sample = t;
            }
        }

        console.log(`Total students with MBBS flag in NCT01: ${mbbsCount}`);
        if (sample) {
            console.log("Sample NCT01 object with MBBS flag:", sample);
        }

    } catch (e) {
        console.error(e);
    } finally {
        await mongoose.disconnect();
    }
}
checkDB();
