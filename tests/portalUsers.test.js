import test from 'node:test';
import assert from 'node:assert/strict';
import express from 'express';
import { createPortalUserService } from '../services/portalUserService.js';
import { createPortalUsersRouter } from '../routes/portalUsers.js';
function fakeModel() {
  const records = new Map();
  const copy = value => value ? structuredClone(value) : null;
  return {
    findById: id => ({ lean: async () => copy(records.get(id)) }),
    find: query => ({ lean: async () => [...records.values()].filter(r => r.role === query.role).map(copy) }),
    create: async record => { if (records.has(record._id)) throw Object.assign(new Error('duplicate'), { code: 11000 }); records.set(record._id, copy(record)); return copy(record); },
    findOneAndUpdate: (query, update) => ({ lean: async () => {
      const old = records.get(query._id);
      if (!old || !Object.entries(query).every(([k, v]) => old[k] === v)) return null;
      const result = { ...old, ...update.$set }; records.set(query._id, copy(result)); return copy(result);
    } }),
  };
}
test('existing accounts remain available; new role-specific accounts persist, delete and re-add safely', async () => {
  const model = fakeModel(), service = createPortalUserService(model);
  assert.equal((await service.list('centre')).length, 182);
  assert.equal((await service.list('admin')).length, 8);
  const input = { userId: ' TEST.USER@CSRL.IN ', name: 'New User', centres: [' agr ', 'AGR'] };
  const added = await service.add('centre', input, 'operator');
  assert.equal(added.userId, 'test.user@csrl.in'); assert.deepEqual(added.centres, ['AGR']);
  await assert.rejects(service.add('centre', input, 'operator'), e => e.status === 409);
  const management = await service.add('admin', input, 'operator');
  assert.equal((await createPortalUserService(model).list('centre')).length, 183);
  assert.equal((await service.list('admin')).length, 9);
  if (process.env.TEST_CENTRE_PASSWORD && process.env.TEST_MANAGEMENT_PASSWORD) {
    assert.equal((await service.authenticate('centre', input.userId, process.env.TEST_CENTRE_PASSWORD))?.id, added.userId);
    assert.equal((await service.authenticate('admin', input.userId, process.env.TEST_MANAGEMENT_PASSWORD))?.id, management.userId);
    assert.equal(await service.authenticate('admin', input.userId, process.env.TEST_CENTRE_PASSWORD), null);
    assert.equal(await service.authenticate('centre', input.userId, process.env.TEST_MANAGEMENT_PASSWORD), null);
    assert.ok(await service.authenticate('centre', 'anirban.das@csrl.in', process.env.TEST_CENTRE_PASSWORD));
    assert.ok(await service.authenticate('admin', 'diropr@csrl.in', process.env.TEST_MANAGEMENT_PASSWORD));
  }
  const token = { role: 'centre', loginUserId: added.userId, accountVersion: added.version };
  assert.equal(await service.isTokenActive(token), true);
  await service.remove('centre', added.userId, added.version, 'operator');
  assert.equal(await service.isTokenActive(token), false);
  assert.equal(await service.authenticate('centre', added.userId, process.env.TEST_CENTRE_PASSWORD || 'wrong'), null);
  assert.equal((await service.list('admin')).length, 9);
  const replacement = await service.add('centre', input, 'operator');
  assert.notEqual(replacement.version, added.version);
  assert.equal(await service.isTokenActive(token), false);
  await assert.rejects(service.remove('centre', added.userId, added.version, 'operator'), e => e.status === 409);
  assert.equal(await service.isTokenActive({ ...token, accountVersion: replacement.version }), true);
});
test('deleted original IDs stay disabled after reload; stale baseline tokens cannot revive', async () => {
  const model = fakeModel(), service = createPortalUserService(model);
  const token = { role: 'centre', loginUserId: 'anirban.das@csrl.in' };
  assert.equal(await service.isTokenActive(token), true);
  await service.remove('centre', token.loginUserId, 'baseline', 'operator');
  const reloaded = createPortalUserService(model);
  assert.equal(await reloaded.isTokenActive(token), false);
  assert.equal((await reloaded.list('centre')).length, 181);
  const added = await reloaded.add('centre', { userId: token.loginUserId, name: 'Restored User', centres: ['AGR'] }, 'operator');
  assert.notEqual(added.version, 'baseline'); assert.equal(await reloaded.isTokenActive(token), false);
  assert.equal(await reloaded.isTokenActive({ role: 'admin', id: 'admin' }), true);
});
test('validate identifiers and reject reserved IDs, unknown roles and concurrent duplicates', async () => {
  const service = createPortalUserService(fakeModel());
  for (const role of ['student', '__proto__']) await assert.rejects(service.list(role), e => e.status === 400);
  for (const id of ['admin', 'centre', 'bad id', '<script>']) await assert.rejects(service.add('admin', { userId: id, name: 'Name', centres: [] }, 'operator'), e => e.status === 400);
  const input = { userId: 'parallel@csrl.in', name: 'Parallel', centres: [] };
  const results = await Promise.allSettled([service.add('centre', input, 'operator'), service.add('centre', input, 'operator')]);
  assert.equal(results.filter(r => r.status === 'fulfilled').length, 1);
  assert.equal(results.find(r => r.status === 'rejected').reason.status, 409);
});
test('user-management API enforces roles, prevents self-deletion and returns no password data', async () => {
  const service = createPortalUserService(fakeModel());
  const app = express(); app.use(express.json());
  app.use((req, _res, next) => { req.user = { role: req.headers['x-role'] || 'centre', loginUserId: 'diropr@csrl.in' }; next(); });
  app.use('/users', createPortalUsersRouter(service));
  const server = app.listen(0, '127.0.0.1'); await new Promise(r => server.once('listening', r));
  const url = `http://127.0.0.1:${server.address().port}/users`;
  const headers = { 'Content-Type': 'application/json', 'x-role': 'admin' };
  try {
    for (const method of ['GET', 'POST', 'DELETE']) assert.equal((await fetch(url + '?role=centre', { method })).status, 403);
    const list = await (await fetch(url + '?role=centre', { headers })).json();
    assert.equal(list.users.length, 182); assert.ok(!JSON.stringify(list).includes('password'));
    let response = await fetch(url, { method: 'POST', headers, body: JSON.stringify({ role: 'admin', userId: 'created@csrl.in', name: 'Created', centres: ['H.O.'] }) });
    assert.equal(response.status, 201); const { user } = await response.json();
    response = await fetch(url, { method: 'DELETE', headers, body: JSON.stringify({ role: 'admin', userId: 'diropr@csrl.in', version: 'baseline' }) });
    assert.equal(response.status, 400);
    response = await fetch(url, { method: 'DELETE', headers, body: JSON.stringify(user) });
    assert.equal(response.status, 200);
    assert.equal((await service.list('admin')).length, 8);
  } finally { await new Promise(r => server.close(r)); }
});
