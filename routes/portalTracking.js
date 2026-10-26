import express from 'express';
import Session from '../models/PortalLoginSession.js';
import { advanceSession, publicSession } from '../services/portalTracking.js';
const router = express.Router();
router.use((_req, res, next) => { res.set('Cache-Control', 'no-store'); next(); });
async function updatePresence(req, res, end) {
  if (!['centre', 'admin'].includes(req.user.role) || !req.user.portalSessionId) return res.status(403).json({ message: 'Tracked portal login required' });
  try {
    // Compare-and-swap prevents concurrent tabs/retries from counting time twice.
    for (let attempt = 0; attempt < 5; attempt++) {
      const s = await Session.findOne({ _id: req.user.portalSessionId, userId: req.user.loginUserId }).lean();
      if (!s) return res.sendStatus(404);
      if (s.endedAt) return res.sendStatus(410);
      const updated = await Session.findOneAndUpdate({ _id: s._id, revision: s.revision, endedAt: null }, { $set: advanceSession(s, new Date(), req.body.active === true, end) }, { new: true }).lean();
      if (updated) return res.json({ success: true });
    }
    return res.status(409).json({ message: 'Retry heartbeat' });
  } catch { return res.status(503).json({ message: 'Login tracking temporarily unavailable' }); }
}
router.post('/heartbeat', (req, res) => updatePresence(req, res, false));
router.post('/logout', (req, res) => updatePresence(req, res, true));
router.get('/', async (req, res) => {
  if (req.user.role !== 'admin') return res.status(403).json({ message: 'Management only' });
  try {
    const page = Math.max(1, Math.min(100000, Number.parseInt(req.query.page, 10) || 1));
    if (req.query.view === 'centres') {
      const centres = (await Session.distinct('centres')).filter(value => typeof value === 'string' && value.trim()).sort((a, b) => a.localeCompare(b));
      return res.json({ centres });
    }
    const query = {};
    if (req.query.centre) query.centres = String(req.query.centre).trim();
    if (req.query.userId) query.userId = String(req.query.userId).trim().toLowerCase();
    const search = String(req.query.search || '').trim().slice(0, 120);
    if (search) {
      const escaped = search.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      query.$or = ['userId', 'name', 'centres'].map(field => ({ [field]: { $regex: escaped, $options: 'i' } }));
    }
    if (req.query.from || req.query.to) {
      query.loginAt = {};
      for (const key of ['from', 'to']) if (req.query[key]) {
        const value = String(req.query[key]);
        if (!/^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2})?$/.test(value)) return res.status(400).json({ message: 'Invalid date' });
        const time = value.includes('T') ? `${value}:${key === 'from' ? '00.000' : '59.999'}` : `${value}T${key === 'from' ? '00:00:00.000' : '23:59:59.999'}`;
        const date = new Date(`${time}+05:30`);
        if (!Number.isFinite(date.getTime())) return res.status(400).json({ message: 'Invalid date' });
        query.loginAt[key === 'from' ? '$gte' : '$lte'] = date;
      }
      if (query.loginAt.$gte > query.loginAt.$lte) return res.status(400).json({ message: 'From date must precede to date' });
    }
    if (req.query.view === 'users') {
      const [result] = await Session.aggregate([
        { $match: query },
        { $sort: { loginAt: -1, _id: -1 } },
        { $group: {
          _id: '$userId', name: { $first: '$name' }, centres: { $first: '$centres' },
          roles: { $addToSet: { $ifNull: ['$role', 'centre'] } },
          loginCount: { $sum: 1 }, activeMs: { $sum: '$activeMs' },
        } },
        { $facet: {
          rows: [{ $sort: { activeMs: -1, _id: 1 } }, { $skip: (page - 1) * 50 }, { $limit: 50 }],
          totals: [{ $group: { _id: null, users: { $sum: 1 }, loginCount: { $sum: '$loginCount' }, activeMs: { $sum: '$activeMs' } } }],
        } },
      ]);
      const summary = result?.totals[0] || { users: 0, loginCount: 0, activeMs: 0 };
      return res.json({ rows: (result?.rows || []).map(row => ({ ...row, userId: row._id })), total: summary.users, summary, page, pages: Math.max(1, Math.ceil(summary.users / 50)) });
    }
    const [rows, total, summary] = await Promise.all([
      Session.find(query).sort({ loginAt: -1, _id: -1 }).skip((page - 1) * 50).limit(50).lean(),
      Session.countDocuments(query),
      Session.aggregate([{ $match: query }, { $group: { _id: '$userId', sessionMs: { $sum: '$sessionMs' }, activeMs: { $sum: '$activeMs' } } }, { $group: { _id: null, users: { $sum: 1 }, sessionMs: { $sum: '$sessionMs' }, activeMs: { $sum: '$activeMs' } } }]),
    ]);
    res.json({ rows: rows.map(s => publicSession(s)), total, page, pages: Math.max(1, Math.ceil(total / 50)), summary: summary[0] || { users: 0, sessionMs: 0, activeMs: 0 } });
  } catch { res.status(503).json({ message: 'Unable to load login tracking. Please retry.' }); }
});
export default router;
