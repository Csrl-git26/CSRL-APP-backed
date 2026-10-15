import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import express from 'express';
import { advanceSession, publicSession } from '../services/portalTracking.js';
import { authenticateCentreUser } from '../services/centreUserAuth.js';
import Session from '../models/PortalLoginSession.js';
import { authenticateManagementUser } from '../services/managementUserAuth.js';
import router from '../routes/portalTracking.js';
const start = new Date('2026-10-15T00:00:00Z');
const base = () => ({ _id: 'session', userId: 'person@example.org', revision: 0, loginAt: start, lastSeenAt: start, sessionMs: 0, activeMs: 0 });
test('active, idle and disconnected time; logout and estimated status', () => {
  let s = { ...base(), ...advanceSession(base(), start, true) };
  s = { ...s, ...advanceSession(s, new Date(+start + 30000), true) };
  assert.equal(s.activeMs, 30000); assert.equal(s.sessionMs, 30000);
  s = { ...s, ...advanceSession(s, new Date(+start + 60000), false) };
  s = { ...s, ...advanceSession(s, new Date(+start + 90000), false) };
  assert.equal(s.activeMs, 65000); assert.equal(s.sessionMs, 90000);
  s = { ...s, ...advanceSession(s, new Date(+start + 3600000), true) };
  assert.equal(s.activeMs, 65000); assert.equal(s.sessionMs, 90000);
  assert.equal(publicSession(s, +start + 3800000).endIsEstimated, true);
  s = { ...s, ...advanceSession(s, new Date(+start + 3630000), false, true) };
  assert.equal(publicSession(s).status, 'Logged out'); assert.equal(s.activeMs, 95000);
});
test('duplicate heartbeat at the same time cannot add duration twice', () => {
  let s = { ...base(), ...advanceSession(base(), start, true) };
  s = { ...s, ...advanceSession(s, new Date(+start + 30000), true) };
  const duplicate = advanceSession(s, new Date(+start + 30000), true);
  assert.equal(duplicate.activeMs, s.activeMs); assert.equal(duplicate.sessionMs, s.sessionMs);
});
test('directory has unique ids and auth rejects unknown or wrong passwords', () => {
  const directory = JSON.parse(fs.readFileSync(new URL('../config/centreUsers.json', import.meta.url)));
  assert.equal(directory.users.length, 182);
  assert.equal(new Set(directory.users.map(u => u.id)).size, 182);
  assert.equal(authenticateCentreUser('unknown@example.org', 'invalid'), null);
  assert.equal(authenticateCentreUser('anirban.das@csrl.in', 'invalid'), null);
  if (process.env.TEST_CENTRE_PASSWORD) for (const user of directory.users) {
    assert.equal(authenticateCentreUser(` ${user.id.toUpperCase()} `, process.env.TEST_CENTRE_PASSWORD)?.id, user.id);
  }
});
test('tracking endpoints enforce roles, identity, logout and date validation', async () => {
  const app = express(); app.use(express.json());
  app.use((req, _res, next) => { req.user = { role: req.headers['x-role'] || 'student', portalSessionId: req.headers['x-untracked'] ? undefined : 'session', loginUserId: 'person@example.org' }; next(); });
  app.use('/tracking', router);
  const server = app.listen(0, '127.0.0.1');
  await new Promise(resolve => server.once('listening', resolve));
  const url = `http://127.0.0.1:${server.address().port}/tracking`;
  const originalFind = Session.findOne; const originalUpdate = Session.findOneAndUpdate;
  let stored = base();
  Session.findOne = query => ({ lean: async () => { assert.equal(query.userId, stored.userId); return { ...stored }; } });
  Session.findOneAndUpdate = (query, update) => ({ lean: async () => {
    if (query.revision !== stored.revision) return null;
    stored = { ...stored, ...update.$set }; return { ...stored };
  } });
  try {
    assert.equal((await fetch(url)).status, 403);
    assert.equal((await fetch(url, { headers: { 'x-role': 'centre' } })).status, 403);
    assert.equal((await fetch(url + '?from=bad', { headers: { 'x-role': 'admin' } })).status, 400);
    assert.equal((await fetch(url + '/heartbeat', { method: 'POST', headers: { 'content-type': 'application/json', 'x-role': 'student' }, body: '{}' })).status, 403);
    assert.equal((await fetch(url + '/heartbeat', { method: 'POST', headers: { 'content-type': 'application/json', 'x-role': 'admin', 'x-untracked': '1' }, body: '{}' })).status, 403);
    const adminOptions = { method: 'POST', headers: { 'content-type': 'application/json', 'x-role': 'admin' }, body: '{"active":true}' };
    assert.equal((await fetch(url + '/heartbeat', adminOptions)).status, 200);
    const options = { method: 'POST', headers: { 'content-type': 'application/json', 'x-role': 'centre' }, body: '{"active":true,"userId":"forged"}' };
    assert.equal((await fetch(url + '/heartbeat', options)).status, 200);
    assert.equal((await fetch(url + '/logout', options)).status, 200);
    assert.equal((await fetch(url + '/heartbeat', options)).status, 410);
    assert.equal(stored.userId, 'person@example.org');
  } finally {
    Session.findOne = originalFind; Session.findOneAndUpdate = originalUpdate;
    await new Promise(resolve => server.close(resolve));
  }
});

test('all listed management accounts validate with their password and reject incorrect credentials', () => {
  const directory = JSON.parse(fs.readFileSync(new URL('../config/managementUsers.json', import.meta.url)));
  assert.equal(directory.users.length, 8);
  assert.equal(new Set(directory.users.map(u => u.id)).size, 8);
  assert.equal(authenticateManagementUser('unknown@example.org', 'invalid'), null);
  for (const user of directory.users) {
    assert.equal(authenticateManagementUser(user.id, 'invalid'), null);
    assert.equal(authenticateCentreUser(user.id, 'invalid'), null);
    if (process.env.TEST_MANAGEMENT_PASSWORD) {
      assert.equal(authenticateManagementUser(` ${user.id.toUpperCase()} `, process.env.TEST_MANAGEMENT_PASSWORD)?.id, user.id);
    }
  }
});
test('user totals support IST time selection and exact-user drilldown', async () => {
  const app = express();
  app.use((req, _res, next) => { req.user = { role: 'admin' }; next(); });
  app.use('/tracking', router);
  const server = app.listen(0, '127.0.0.1');
  await new Promise(resolve => server.once('listening', resolve));
  const url = `http://127.0.0.1:${server.address().port}/tracking`;
  const originalAggregate = Session.aggregate;
  let match;
  Session.aggregate = async pipeline => {
    match = pipeline[0].$match;
    assert.equal(pipeline[2].$group._id, '$userId');
    assert.equal(pipeline[2].$group.activeMs.$sum, '$activeMs');
    return [{ rows: [{ _id: 'person@example.org', name: 'Person', centres: ['AGR'], roles: ['centre'], loginCount: 2, activeMs: 90000 }], totals: [{ users: 1, loginCount: 2, activeMs: 90000 }] }];
  };
  try {
    const result = await (await fetch(url + '?view=users&from=2026-10-15T09:30&to=2026-10-15T10:15&userId=PERSON%40EXAMPLE.ORG')).json();
    assert.equal(match.userId, 'person@example.org');
    assert.equal(match.loginAt.$gte.toISOString(), '2026-10-15T04:00:00.000Z');
    assert.equal(match.loginAt.$lte.toISOString(), '2026-10-15T04:45:59.999Z');
    assert.equal(result.rows[0].userId, 'person@example.org');
    assert.equal(result.summary.loginCount, 2);
    assert.equal(result.summary.activeMs, 90000);
    assert.equal(result.total, 1);
    assert.equal((await fetch(url + '?from=2026-10-16T10:00&to=2026-10-15T10:00')).status, 400);
  } finally {
    Session.aggregate = originalAggregate;
    await new Promise(resolve => server.close(resolve));
  }
});
