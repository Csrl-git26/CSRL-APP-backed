import fs from 'fs';
const file = '/Users/surya/Desktop/CSRL-APP-backed/services/dbService.js';
let content = fs.readFileSync(file, 'utf8');

content = content.replace(
  /{ ROLL_KEY: { \$in: Array.from(relevantRollKeys) } }/,
  `{ ROLL_KEY: { $in: [...Array.from(relevantRollKeys), ...Array.from(relevantRollKeys).map(k => Number(k)).filter(k => !isNaN(k))] } }`
);

fs.writeFileSync(file, content);
console.log("Fixed type coercion in Profile.find");
