import './bootstrap-env.js';
import { initMongo } from './services/mongoInit.js';
import StudentRawMarks from './models/StudentRawMarks.js';
import TopicMap from './models/TopicMap.js';
import StudentWeakTopics from './models/StudentWeakTopics.js';
import StudentOverallWeakTopics from './models/StudentOverallWeakTopics.js';

await initMongo();

// 1. What testIds have raw marks?
const rawGroups = await StudentRawMarks.aggregate([
  { $group: { _id: '$testId', count: { $sum: 1 } } },
  { $sort: { _id: 1 } }
]);
console.log('\n📊 StudentRawMarks by testId:');
for (const g of rawGroups) console.log(`  testId="${g._id}"  students=${g.count}`);

// 2. What TopicMaps exist?
const maps = await TopicMap.find({}).lean();
console.log('\n🗺️  TopicMaps:');
for (const m of maps) {
  const qCount = m.topics.reduce((s,t) => s + t.questions.length, 0);
  console.log(`  testId="${m.testId}"  topics=${m.topics.length}  questions=${qCount}`);
}

// 3. What StudentWeakTopics exist?
const swtGroups = await StudentWeakTopics.aggregate([
  { $group: { _id: '$testId', count: { $sum: 1 } } },
  { $sort: { _id: 1 } }
]);
console.log('\n💡 StudentWeakTopics by testId:');
for (const g of swtGroups) console.log(`  testId="${g._id}"  docs=${g.count}`);

// 4. StudentOverallWeakTopics sample
const overall = await StudentOverallWeakTopics.find({}).limit(5).lean();
console.log(`\n🏁 StudentOverallWeakTopics total docs: ${await StudentOverallWeakTopics.countDocuments()}`);
if (overall.length > 0) {
  const s = overall[0];
  console.log(`  Sample: studentId="${s.studentId}"  strong=${s.strongTopics?.length}  moderate=${s.moderateTopics?.length}  weak=${s.weakTopics?.length}`);
  console.log(`  subjectWise keys: ${JSON.stringify(Object.keys(s.subjectWise || {}))}`);
}

// 5. Check if student 2701073 has any data
const rohit = await StudentWeakTopics.find({ studentId: '2701073' }).lean();
console.log(`\n🎯 WeakTopics for roll 2701073: ${rohit.length} doc(s)`);
for (const r of rohit) {
  console.log(`  testId="${r.testId}" strong=${r.strongTopics?.length} moderate=${r.moderateTopics?.length} weak=${r.weakTopics?.length}`);
}

const rohitOverall = await StudentOverallWeakTopics.findOne({ studentId: '2701073' }).lean();
console.log(`  OverallWeakTopics: ${rohitOverall ? 'EXISTS' : 'MISSING'}`);
if (rohitOverall) {
  console.log(`  strong=${rohitOverall.strongTopics?.length} moderate=${rohitOverall.moderateTopics?.length} weak=${rohitOverall.weakTopics?.length}`);
}

// 6. Sample a raw marks doc — show what Q columns look like
const sampleRaw = await StudentRawMarks.findOne({}).lean();
if (sampleRaw) {
  const marks = sampleRaw.marks instanceof Map 
    ? Object.fromEntries(sampleRaw.marks) 
    : sampleRaw.marks;
  const keys = Object.keys(marks || {}).slice(0, 10);
  console.log(`\n📋 Sample raw marks doc — testId="${sampleRaw.testId}" studentId="${sampleRaw.studentId}"`);
  console.log(`  Question columns (first 10): ${JSON.stringify(keys)}`);
  console.log(`  Sample values: ${JSON.stringify(keys.map(k => marks[k]))}`);
}

process.exit(0);
