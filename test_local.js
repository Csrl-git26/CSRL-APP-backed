import fs from 'fs';

// Check if rawScores is inside TestInsightsPanel
const frontendCode = fs.readFileSync('/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestInsightsPanel.jsx', 'utf8');
if (frontendCode.includes('r.rawScores')) {
  console.log('Frontend has r.rawScores');
} else {
  console.log('Frontend MISSING r.rawScores');
}
