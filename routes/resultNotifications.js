import express from 'express';
import { createHash } from 'node:crypto';
import ResultNotification from '../models/ResultNotification.js';
import { portalUsers } from '../services/portalUserService.js';
import { SENDER, PORTAL, renderEmail, reportWorkbook } from '../services/resultNotificationEmail.js';
const hash = value => createHash('sha256').update(value).digest('hex');
const fail = (status, message) => Object.assign(new Error(message), { status });
export const configured = () => process.env.RESULT_EMAIL_ENABLED === 'true' && !!process.env.RESEND_API_KEY;
export function validateSelection(input = {}) {
  const { testKey, stream, testDate, audience } = input;
  const branch = stream === 'NEET' ? null : input.branch;
  if (typeof testKey !== 'string' || !testKey.trim() || testKey.length > 100 || /[,\r\n\x00$]/.test(testKey) || testKey === 'ALL_FMT') throw fail(400, 'Select one saved test.');
  if (!['JEE','NEET'].includes(stream) || (stream === 'JEE' && !['MAIN','ADVANCED'].includes(branch))) throw fail(400, 'Select a valid stream and branch.');
  if (typeof testDate !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(testDate) || !Number.isFinite(Date.parse(testDate)) || new Date(testDate).toISOString().slice(0,10) !== testDate) throw fail(400, 'Enter a valid test date.');
  if (!['all','centre','admin'].includes(audience)) throw fail(400, 'Select a recipient group.');
  return { testKey: testKey.trim(), stream, branch, testDate, audience };
}
export async function recipientList(audience, service = portalUsers) {
  const roles = audience === 'all' ? ['centre','admin'] : [audience];
  const recipients = new Map(), skipped = new Set();
  for (const role of roles) for (const user of await service.list(role)) {
    const email = String(user.userId || '').trim().toLowerCase();
    if (!/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(email)) { skipped.add(email); continue; }
    if (!recipients.has(email)) recipients.set(email, { email, name: user.name || email, roles: [], status: 'pending' });
    recipients.get(email).roles.push(role);
  }
  return { recipients: [...recipients.values()].sort((a,b) => a.email.localeCompare(b.email)), skippedUsers: [...skipped].sort() };
}
export function publicCampaign(c, preview = false) {
  return { id: c._id, selection: c.selection, subject: c.subject, state: c.state, createdAt: c.createdAt,
    warnings: c.report?.warnings || [], skippedUsers: c.skippedUsers || [], filename: c.filename,
    counts: Object.fromEntries(['pending','sending','sent','failed','review','skipped'].map(status => [status, c.recipients.filter(r => r.status === status).length])),
    recipients: c.recipients.map(({ email, name, status, error }) => ({ email, name, status, error })),
    ...(preview ? { html: c.html } : {}),
  };
}
export function createResultNotificationsRouter(buildReport, { Model = ResultNotification, service = portalUsers } = {}) {
  const router = express.Router();
  router.use((req,res,next) => { res.set('Cache-Control','no-store'); if (req.user?.role !== 'admin') return res.status(403).json({ message: 'Admin access required.' }); next(); });
  const wrap = fn => async (req,res) => { try { await fn(req,res); } catch(e) { res.status(e.status || 503).json({ message: e.status ? e.message : 'Notification service unavailable. Please retry.' }); } };
  const get = async id => { if (!/^[a-f0-9]{64}$/.test(id)) throw fail(404,'Notification not found.'); const c = await Model.findById(id).lean(); if (!c) throw fail(404,'Notification not found.'); return c; };
  router.get('/', wrap(async (req,res) => {
    const campaigns = await Model.find({}).sort({ createdAt: -1 }).limit(20).select('-attachment -html -text').lean();
    res.json({ configured: configured(), sender: SENDER, campaigns: campaigns.map(c => publicCampaign(c)) });
  }));
  router.post('/preview', wrap(async (req,res) => {
    const selection = validateSelection(req.body);
    const report = await buildReport(selection);
    if (!report.rows?.length || !report.overall?.appeared) throw fail(400,'No results found for this test and stream.');
    const list = await recipientList(selection.audience, service);
    const email = renderEmail(selection, report);
    const id = hash(JSON.stringify({ selection, report, emails: list.recipients.map(r => r.email), email }));
    let campaign = await Model.findById(id).lean();
    if (!campaign) {
      const attachment = (await reportWorkbook(report)).toString('base64');
      if (attachment.length > 10_000_000) throw fail(400, 'Report too large to email.');
      const record = { _id: id, selection, report, ...email, ...list, attachment, filename: `${selection.testKey.replace(/[^a-zA-Z0-9_-]/g,'_')}-centre-analysis.xlsx`, createdBy: req.user.loginUserId || req.user.id, state: 'draft' };
      try { await Model.create(record); } catch(e) { if (e.code !== 11000) throw e; }
      campaign = await Model.findById(id).lean();
    }
    res.json({ campaign: publicCampaign(campaign,true), configured: configured(), sender: SENDER });
  }));
  router.get('/:id', wrap(async (req,res) => res.json({ campaign: publicCampaign(await get(req.params.id),true) })));
  router.get('/:id/attachment', wrap(async (req,res) => {
    const c = await get(req.params.id);
    res.type('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet').attachment(c.filename).send(Buffer.from(c.attachment,'base64'));
  }));
  router.post('/:id/send', wrap(async (req,res) => {
    if (!configured()) throw fail(503,'Email setup is incomplete. Verify csrl.in in Resend and set the Render environment variables.');
    if (req.body.confirm !== 'SEND') throw fail(400,'Confirm the reviewed email and recipient list before sending.');
    const c = await get(req.params.id);
    if (c.report?.warnings?.length) throw fail(400,'Resolve the report warnings and preview again before sending.');
    if (!c.recipients.length) throw fail(400,'No valid recipient email addresses.');
    await Model.updateOne({ _id: c._id, state: 'draft' }, { $set: { state: 'queued', startedAt: new Date() } });
    res.json({ campaign: publicCampaign(await get(c._id)) });
  }));
  router.post('/:id/retry', wrap(async (req,res) => {
    if (!configured()) throw fail(503,'Email sending is not configured.');
    if (req.body.confirm !== 'RETRY') throw fail(400,'Confirm retry of failed recipients.');
    const c = await get(req.params.id);
    if (c.state === 'draft') throw fail(400,'Review and send the draft first.');
    await Model.updateOne({ _id: c._id, 'recipients.status': 'failed' }, { $set: { state: 'queued', 'recipients.$[recipient].status': 'pending', 'recipients.$[recipient].error': '' } }, { arrayFilters: [{ 'recipient.status': 'failed' }] });
    res.json({ campaign: publicCampaign(await get(c._id)) });
  }));
  return router;
}
// Durable outbox: the UI never loops over recipients or supplies arbitrary addresses.
export function createNotificationWorker({ Model = ResultNotification, service = portalUsers, send = (...args) => fetch(...args), enabled = configured } = {}) {
  let working = false;
  return async function tick() {
    if (working || !enabled()) return;
    working = true;
    try {
      const c = await Model.findOne({ state: 'queued' }).sort({ startedAt: 1 }).lean();
      if (!c) return;
      const now = new Date();
      const recipient = c.recipients.find(r => r.status === 'pending' || (r.status === 'sending' && new Date(r.lockUntil) <= now));
      if (!recipient) {
        await Model.updateOne({ _id: c._id, state: 'queued', recipients: { $not: { $elemMatch: { status: { $in: ['pending','sending'] } } } } }, { $set: { state: 'complete' } });
        return;
      }
      const firstAttempt = recipient.firstAttempt || now;
      const lockUntil = new Date(now.getTime()+120000);
      const claim = await Model.updateOne({ _id: c._id, state: 'queued', recipients: { $elemMatch: { email: recipient.email, $or: [{ status: 'pending' }, { status: 'sending', lockUntil: { $lte: now } }] } } }, { $set: { 'recipients.$.status': 'sending', 'recipients.$.firstAttempt': firstAttempt, 'recipients.$.lockUntil': lockUntil } });
      if (!claim.modifiedCount) return;
      const finish = values => Model.updateOne({ _id: c._id, recipients: { $elemMatch: { email: recipient.email, status: 'sending', lockUntil } } }, { $set: Object.fromEntries(Object.entries(values).map(([key,value]) => ['recipients.$.'+key,value])) });
      if (now - new Date(firstAttempt) > 23*60*60*1000) { await finish({ status: 'review', error: 'Retry window expired. Check provider logs before sending again.' }); return; }
      try {
        const active = await recipientList(c.selection.audience, service);
        if (!active.recipients.some(r => r.email === recipient.email)) { await finish({ status: 'skipped', error: 'User is no longer in the selected active directory.' }); return; }
        const response = await send('https://api.resend.com/emails', {
          method: 'POST', signal: AbortSignal.timeout(20000),
          headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json', 'Idempotency-Key': `result/${c._id}/${hash(recipient.email).slice(0,24)}` },
          body: JSON.stringify({ from: `${PORTAL} <${SENDER}>`, to: [recipient.email], subject: c.subject, html: c.html, text: c.text, attachments: [{ filename: c.filename, content: c.attachment }] }),
        });
        const result = await response.json().catch(() => ({}));
        if (!response.ok || !result.id) throw new Error(`Email provider rejected the request (${response.status}). Check Resend logs and setup.`);
        await finish({ status: 'sent', providerId: result.id, error: '' });
      } catch(e) { await finish({ status: 'failed', error: e.name === 'TimeoutError' ? 'Provider timeout. Retry uses the same duplicate-protection key.' : e.message.startsWith('Email provider') ? e.message : 'Unable to confirm sending. Retry within 23 hours or check provider logs.' }); }
    } catch(e) { console.error('Result notification worker:', e.message); }
    finally { working = false; }
  };
}
export function startNotificationWorker() { const tick = createNotificationWorker(); const timer = setInterval(tick,1500); timer.unref(); return timer; }
