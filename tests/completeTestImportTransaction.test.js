import test from 'node:test';
import assert from 'node:assert/strict';
import mongoose from 'mongoose';
import Profile from '../models/Profile.js';
import TestScore from '../models/TestScore.js';
import { replaceCompleteTest } from '../services/completeTestImport.js';

const input = { testKey: 'MT01', stream: 'JEE', marks: [{ rollKey: '1', centerCode: 'KNP', scores: { MT01: 150 } }] };

test('replacement writes backups and score operations in the same transaction', async t => {
  const calls = [];
  const session = { withTransaction: async fn => fn(), endSession: async () => calls.push('closed') };
  t.mock.method(mongoose, 'startSession', async () => session);
  t.mock.method(Profile, 'find', () => ({ session: s => { assert.equal(s, session); return { lean: async () => [{ ROLL_KEY: '1', centerCode: 'KNP', stream: 'JEE' }] }; } }));
  t.mock.method(TestScore, 'find', () => ({ session: () => ({ lean: async () => [{ _id: 'old', ROLL_KEY: '2', centerCode: 'DDN', stream: 'JEE', tests: { MT01: { total: 20 }, MT02: { total: 70 } } }] }) }));
  t.mock.method(mongoose.connection, 'collection', name => {
    assert.equal(name, 'testimportbackups');
    return { insertMany: async (docs, options) => { assert.equal(options.session, session); assert.equal(docs.length, 2); assert.equal(docs[0].before.tests.MT02.total, 70); calls.push('backup'); } };
  });
  t.mock.method(TestScore, 'bulkWrite', async (ops, options) => {
    assert.equal(options.session, session);
    assert.deepEqual(ops[0].updateOne.update, { $unset: { 'tests.MT01': '' } });
    assert.equal(ops[1].insertOne.document.tests.MT01.total, 150);
    calls.push('scores');
  });
  assert.equal((await replaceCompleteTest(input)).importedCount, 1);
  assert.deepEqual(calls, ['backup', 'scores', 'closed']);
});

test('validation failure closes the session without writing a backup or scores', async t => {
  let closed = false;
  t.mock.method(mongoose, 'startSession', async () => ({ withTransaction: async fn => fn(), endSession: async () => { closed = true; } }));
  t.mock.method(Profile, 'find', () => ({ session: () => ({ lean: async () => [] }) }));
  t.mock.method(TestScore, 'bulkWrite', () => assert.fail('must not write invalid input'));
  t.mock.method(mongoose.connection, 'collection', () => assert.fail('must not archive invalid input'));
  await assert.rejects(replaceCompleteTest(input), /unique matching student/);
  assert.equal(closed, true);
});

test('a failed backup prevents score changes', async t => {
  t.mock.method(mongoose, 'startSession', async () => ({ withTransaction: async fn => fn(), endSession: async () => {} }));
  t.mock.method(Profile, 'find', () => ({ session: () => ({ lean: async () => [{ ROLL_KEY: '1', centerCode: 'KNP', stream: 'JEE' }] }) }));
  t.mock.method(TestScore, 'find', () => ({ session: () => ({ lean: async () => [] }) }));
  t.mock.method(mongoose.connection, 'collection', () => ({ insertMany: async () => { throw new Error('backup failed'); } }));
  t.mock.method(TestScore, 'bulkWrite', () => assert.fail('must not write without backup'));
  await assert.rejects(replaceCompleteTest(input), /backup failed/);
});
