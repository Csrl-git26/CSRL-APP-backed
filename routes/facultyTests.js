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
export default router;
