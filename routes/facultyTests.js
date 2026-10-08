import express from 'express';
import FacultyTestResult from '../models/FacultyTestResult.js';
import { validateFacultyResults } from '../services/facultyResults.js';
const router = express.Router();
router.use((req,res,next) => ['admin','centre'].includes(req.user?.role) ? next() : res.status(403).json({ message: 'Management or centre access required.' }));
router.get('/', async (req,res) => {
  try {
    const query = req.user.role === 'centre' && req.user.id !== 'centre' ? { centres: req.user.centerCode || '__NO_CENTRE__' } : {};
    const rows = await FacultyTestResult.find(query).select('-__v').lean();
    res.json({ rows });
  } catch { res.status(500).json({ message: 'Unable to load faculty results.' }); }
});
router.post('/import', async (req,res) => {
  if (req.user.role !== 'admin') return res.status(403).json({ message: 'Management upload only.' });
  let rows;
  try { rows = validateFacultyResults(req.body.rows); } catch(error) { return res.status(400).json({ message: error.message }); }
  try {
    await FacultyTestResult.bulkWrite(rows.map(row => ({ updateOne: { filter: { year: row.year, email: row.email, test: row.test, subject: row.subject }, update: { $set: row }, upsert: true } })));
    res.json({ count: rows.length });
  } catch { res.status(500).json({ message: 'Import could not finish. Please retry the same file; existing results will not be duplicated.' }); }
});
router.post('/delete', async (req,res) => {
  if (req.user.role !== 'admin') return res.status(403).json({ message: 'Admin access required.' });
  const { year, test, ids, confirmation } = req.body || {};
  if (typeof year !== 'string' || !year.trim() || year === 'ALL' ||
      typeof test !== 'string' || !test.trim() || test === 'ALL' ||
      confirmation !== 'DELETE' || !Array.isArray(ids) || !ids.length || ids.length > 10000 ||
      ids.some(id => typeof id !== 'string' || !/^[a-f0-9]{24}$/i.test(id))) {
    return res.status(400).json({ message: 'Select an academic year and test, review the records, and confirm deletion.' });
  }
  try {
    const result = await FacultyTestResult.deleteMany({ year, test, _id: { $in: ids } });
    res.json({ deletedCount: result.deletedCount });
  } catch { res.status(500).json({ message: 'Unable to delete faculty results. Reload before retrying.' }); }
});
export default router;
