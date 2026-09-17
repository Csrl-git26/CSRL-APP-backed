import mongoose from 'mongoose';
import TopicMap from './models/TopicMap.js';
import CenterOverallWeakTopics from './models/CenterOverallWeakTopics.js';

async function run() {
  try {
    await mongoose.connect('mongodb+srv://admin:YtL8ZtOaJ2sA8E6@csrl-app.2e1i8.mongodb.net/csrl_db?retryWrites=true&w=majority');
    const topicMaps = await TopicMap.find({ testId: 'CMT01' }).lean();
    console.log("TopicMaps:", topicMaps.length);
    const overall = await CenterOverallWeakTopics.find({}).lean();
    console.log("Overall:", overall.length);
    process.exit(0);
  } catch(e) {
    console.error(e);
    process.exit(1);
  }
}
run();
