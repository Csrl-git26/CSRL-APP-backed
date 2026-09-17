import { parseTestColumn } from './utils/testColumns.js';

const doc = {
  "ROLL_KEY": "123",
  "NCT01_PHY": 100,
  "NCT01_CHEM": 120,
  "NCT01_BOT": 140,
  "NCT01_ZOO": 130
};

const validTestKeys = ['NCT01'];
const rKeys = Object.keys(doc);
const getScore = (sub) => {
   for (const rk of rKeys) {
     const p = parseTestColumn(rk);
     if (validTestKeys.includes(p.testName) && p.subject === sub) {
        const val = Number(doc[rk]);
        if (!isNaN(val)) return val > 0 ? val : 0;
     }
   }
   return null;
};

console.log('Physics:', getScore('Physics'));
console.log('Botany:', getScore('Botany'));
