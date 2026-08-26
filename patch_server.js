import fs from 'fs';
const file = '/Users/surya/Desktop/CSRL-APP-backed/server.js';
let content = fs.readFileSync(file, 'utf-8');

const oldRankingsLogic = `  const { testKey, centerCode, limit = '30', order = 'desc' } = req.query;
  if (!testKey) return res.status(400).json({ message: 'testKey is required' });

  const source = centerCode ? await loadCenterApplicationData(centerCode) : await loadApplicationData();`;

const newRankingsLogic = `  const { testKey, limit = '30', order = 'desc' } = req.query;
  if (!testKey) return res.status(400).json({ message: 'testKey is required' });

  // Use the exact same centerCode resolution logic as /api/data/center
  let resolvedCenterCode = req.query.centerCode;
  
  // If no centerCode is provided, fall back to req.user.id (for centre users)
  // If admin/bog requests without centerCode, they might intend to load all, 
  // but if centerCode is truly empty, we loadApplicationData ONLY for admin/bog.
  if (!resolvedCenterCode || resolvedCenterCode === 'undefined' || resolvedCenterCode === 'null') {
    if (req.user.role === 'centre') {
      resolvedCenterCode = req.user.id;
    } else {
      resolvedCenterCode = ''; // Load all for admin/bog
    }
  }

  const source = resolvedCenterCode ? await loadCenterApplicationData(resolvedCenterCode) : await loadApplicationData();`;

content = content.replace(oldRankingsLogic, newRankingsLogic);
fs.writeFileSync(file, content);
console.log("Patched server.js rankings logic");
