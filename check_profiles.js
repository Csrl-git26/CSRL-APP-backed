import { initMongo } from './services/mongoInit.js';
import TopicMap from './models/TopicMap.js';

async function check() {
  await initMongo();
  
  const profiles = await TopicMap.find({}).lean();
  console.log(`Total profiles: ${profiles.length}`);
  
  const jrsProfiles = profiles.filter(p => p.ROLL_KEY && p.ROLL_KEY.includes('JRS'));
  const tezProfiles = profiles.filter(p => p.ROLL_KEY && p.ROLL_KEY.includes('TEZ'));
  
  console.log(`JRS profiles: ${jrsProfiles.length}`);
  if (jrsProfiles.length > 0) {
      console.log('JRS Sample stream:', jrsProfiles[0].stream, jrsProfiles[0].STREAM, jrsProfiles[0].Stream);
  }
  
  console.log(`TEZ profiles: ${tezProfiles.length}`);
  if (tezProfiles.length > 0) {
      console.log('TEZ Sample stream:', tezProfiles[0].stream, tezProfiles[0].STREAM, tezProfiles[0].Stream);
  }
  
  process.exit(0);
}

check();
