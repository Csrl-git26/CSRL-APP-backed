import mongoose from 'mongoose';
import Profile from '../models/Profile.js';
import TestScore from '../models/TestScore.js';
import { validateCompleteTestImport, replacementUpdate } from '../utils/completeTestImport.js';

export async function replaceCompleteTest(input) {
  const session = await mongoose.startSession();
  const importId = new mongoose.Types.ObjectId();
  let count = 0;
  try {
    await session.withTransaction(async () => {
      const profiles = await Profile.find({}).session(session).lean();
      const rows = validateCompleteTestImport(input, profiles);
      const docs = await TestScore.find({}).session(session).lean();
      for (const row of rows) {
        const collisions = docs.filter(d => String(d.ROLL_KEY).trim().toUpperCase() === row.roll);
        if (collisions.length > 1 || collisions.some(d => String(d.centerCode).trim().toUpperCase() !== row.center || String(d.stream || 'JEE').trim().toUpperCase() !== input.stream)) {
          throw Object.assign(new Error(`Roll ${row.roll} has conflicting stored score records. Resolve the centre/stream conflict before replacement.`), { statusCode: 409 });
        }
      }
      const wanted = new Map(rows.map(r => [JSON.stringify([r.center, r.roll]), r]));
      const ops = [], backups = [];
      const seen = new Set();
      for (const doc of docs) {
        if (String(doc.stream || 'JEE').trim().toUpperCase() !== input.stream) continue;
        const key = JSON.stringify([String(doc.centerCode).trim().toUpperCase(), String(doc.ROLL_KEY).trim().toUpperCase()]);
        const row = wanted.get(key);
        if (row && seen.has(key)) throw Object.assign(new Error(`Duplicate stored student ${row.roll}; resolve it before replacing this test.`), { statusCode: 409 });
        if (row) seen.add(key);
        const update = replacementUpdate(doc, input.testKey, row?.scores);
        if (!Object.keys(update).length) continue;
        backups.push({ importId, testKey: input.testKey, stream: input.stream, scoreId: doc._id, before: doc, createdAt: new Date() });
        ops.push({ updateOne: { filter: { _id: doc._id }, update } });
      }
      for (const [key, row] of wanted) {
        if (seen.has(key)) continue;
        const _id = new mongoose.Types.ObjectId();
        backups.push({ importId, testKey: input.testKey, stream: input.stream, scoreId: _id, before: null, createdAt: new Date() });
        ops.push({ insertOne: { document: { _id, ROLL_KEY: row.roll, centerCode: row.center, stream: input.stream, tests: { [input.testKey]: row.scores } } } });
      }
      // Backups and replacements commit together or neither commits.
      await mongoose.connection.collection('testimportbackups').insertMany(backups, { session });
      await TestScore.bulkWrite(ops, { session, ordered: true });
      count = rows.length;
    });
    return { success: true, importedCount: count, backupId: String(importId), mode: 'replace' };
  } finally {
    await session.endSession();
  }
}
