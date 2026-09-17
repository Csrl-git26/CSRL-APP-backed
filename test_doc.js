import fs from 'fs';
const data = JSON.parse(fs.readFileSync('/Users/surya/Desktop/CSRL-APP-backed/data/tests.json', 'utf8'));
console.log(data.find(d => Object.keys(d).some(k => k.includes('CMT01'))));
