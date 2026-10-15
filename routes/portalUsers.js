import express from 'express';
import { portalUsers } from '../services/portalUserService.js';
export function createPortalUsersRouter(service = portalUsers) {
  const router = express.Router();
  router.use((req, res, next) => {
    res.set('Cache-Control', 'no-store');
    if (req.user?.role !== 'admin') return res.status(403).json({ message: 'Admin access required.' });
    next();
  });
  const fail = (res, error) => res.status(error.status || 503).json({ message: error.status ? error.message : 'User management is temporarily unavailable. Please retry.' });
  router.get('/', async (req, res) => {
    try { res.json({ users: await service.list(req.query.role) }); } catch (e) { fail(res, e); }
  });
  router.post('/', async (req, res) => {
    try { res.status(201).json({ user: await service.add(req.body.role, req.body, req.user.loginUserId || req.user.id) }); } catch (e) { fail(res, e); }
  });
  router.delete('/', async (req, res) => {
    if (req.body.role === 'admin' && String(req.body.userId || '').trim().toLowerCase() === req.user.loginUserId) return res.status(400).json({ message: 'You cannot delete the account you are currently using.' });
    try {
      await service.remove(req.body.role, req.body.userId, req.body.version, req.user.loginUserId || req.user.id);
      res.json({ success: true });
    } catch (e) { fail(res, e); }
  });
  return router;
}
export default createPortalUsersRouter();
