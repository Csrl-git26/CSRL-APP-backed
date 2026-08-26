import fs from 'fs';
const file = '/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js';
const content = fs.readFileSync(file, 'utf8');
if (content.includes('rawScores: testDoc || {}')) {
  console.log('rawScores is in backend');
} else {
  console.log('rawScores is NOT in backend');
}
