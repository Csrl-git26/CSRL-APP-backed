import fs from 'fs';

const adminPath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx';
let adminContent = fs.readFileSync(adminPath, 'utf8');

adminContent = adminContent.replace(/return \['ALL_FMT', \.\.\.sorted\];/g, 'return sorted;');
adminContent = adminContent.replace(/return globalStream === 'NEET' \? sorted : \['ALL_FMT', \.\.\.sorted\];/g, 'return sorted;');

fs.writeFileSync(adminPath, adminContent, 'utf8');

const centrePath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx';
let centreContent = fs.readFileSync(centrePath, 'utf8');

centreContent = centreContent.replace(/return \['ALL_FMT', \.\.\.cols\];/g, 'return cols;');
centreContent = centreContent.replace(/return globalStream === 'NEET' \? sorted : \['ALL_FMT', \.\.\.sorted\];/g, 'return sorted;');

fs.writeFileSync(centrePath, centreContent, 'utf8');

console.log("Patched successfully");
