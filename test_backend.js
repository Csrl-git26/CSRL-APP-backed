import { loadCenterApplicationData } from './services/dbService.js';
loadCenterApplicationData("centre").then(data => {
  console.log("Profiles count:", data.profiles.length);
  const p = data.profiles.find(x => String(x.ROLL_KEY) === "2618003");
  console.log("Found profile?", !!p);
}).catch(console.error);
