const fs = require('fs');
const tests = JSON.parse(fs.readFileSync('/Users/surya/Desktop/CSRL-APP-backed/tests.json', 'utf8') || '[]');
console.log(tests.slice(0, 1));
