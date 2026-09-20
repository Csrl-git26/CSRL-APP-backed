import { initMongo } from '../services/mongoInit.js';
import StudentRawMarks from '../models/StudentRawMarks.js';
import {
  computeStudentOverallWeakTopics,
  computeCenterOverallWeakTopics
} from '../services/overallWeakTopicService.js';

async function run() {
  await initMongo();
  console.log('Fetching all raw marks...');
  
  const allDocs = await StudentRawMarks.find({}, { studentId: 1, centerId: 1 }).lean();
  console.log(`Found ${allDocs.length} marks documents.`);
  
  const studentIds = Array.from(new Set(allDocs.map(d => d.studentId)));
  const centerIds = Array.from(new Set(allDocs.map(d => d.centerId).filter(Boolean)));
  
  console.log(`Unique Students: ${studentIds.length}`);
  console.log(`Unique Centers: ${centerIds.length}`);
  
  console.log('Computing student overall analytics...');
  let i = 0;
  for (const sid of studentIds) {
    await computeStudentOverallWeakTopics(sid);
    i++;
    if (i % 50 === 0) console.log(`Processed ${i} students...`);
  }
  
  console.log('Computing center overall analytics...');
  let j = 0;
  for (const cid of centerIds) {
    await computeCenterOverallWeakTopics(cid);
    j++;
    if (j % 5 === 0) console.log(`Processed ${j} centers...`);
  }
  
  console.log('Done!');
  process.exit(0);
}

run().catch(console.error);
