import { AsyncLocalStorage } from 'node:async_hooks';
import mongoose from 'mongoose';
import { parseTestColumn, flatToNested } from '../utils/testColumns.js';

const schema = new mongoose.Schema({
  testId: { type: String, required: true, unique: true },
  stream: { type: String, enum: ['JEE', 'NEET'], required: true },
  branch: { type: String, enum: ['MAIN', 'ADVANCED', null], default: null },
}, { timestamps: true });
export const TestBranch = mongoose.models.TestBranch || mongoose.model('TestBranch', schema);
const requests = new AsyncLocalStorage();
export const currentTestBranch = () => requests.getStore()?.branch;
export function testBranchMiddleware(req, res, next) {
  const branch = req.method === 'GET' ? (req.query.branch || 'MAIN') : undefined;
  if (branch && !['MAIN', 'ADVANCED'].includes(branch)) return res.status(400).json({ message: 'Invalid JEE branch' });
  requests.run({ branch }, next);
}
export function matchesTestBranch(testId, branch, catalog = []) {
  if (!branch) return true;
  const metadata = catalog.find(t => t.testId === testId);
  const stream = metadata?.stream || (/^(MMT|NCT|NMT|NEET)/i.test(testId) ? 'NEET' : 'JEE');
  return stream === 'NEET' || (metadata?.branch || 'MAIN') === branch;
}
async function catalogForRequest() {
  const ctx = requests.getStore();
  if (!ctx?.branch) return [];
  // Keep metadata request-local; never share an in-flight branch selection across users.
  ctx.catalog ||= TestBranch.find({}).lean().exec();
  return ctx.catalog;
}
export async function filterTestDocuments(docs) {
  const branch = currentTestBranch();
  if (!branch) return docs;
  const catalog = await catalogForRequest();
  return docs.filter(d => matchesTestBranch(d.testId, branch, catalog));
}
export const testIdForColumn = col => parseTestColumn(String(col).replace(/_(Attempted|Accuracy|Rank|Correct|Wrong|MBBS|STATUS|ABSENT|GRADE)$/i, '')).testName;
export function scopeApplicationData(data, branch, catalog = []) {
  if (!branch) return data;
  const columns = data.testColumns || [];
  const allowed = columns.filter(c => matchesTestBranch(testIdForColumn(c), branch, catalog));
  const metadataKeys = new Set(['ROLL_KEY', 'centerCode', 'centreCode', 'stream', 'tests', '_id', '__v', 'createdAt', 'updatedAt']);
  return { ...data, testColumns: allowed, tests: (data.tests || []).map(row => {
    const result = Object.fromEntries(Object.entries(row).filter(([key]) => metadataKeys.has(key) || matchesTestBranch(testIdForColumn(key), branch, catalog)));
    if (row.tests) result.tests = Object.fromEntries(Object.entries(row.tests).filter(([key]) => matchesTestBranch(key, branch, catalog)));
    return result;
  }).filter(row => Object.keys(row).some(key => !metadataKeys.has(key)) || Object.keys(row.tests || {}).length > 0) };
}
export async function filterApplicationData(data) {
  const branch = currentTestBranch();
  return branch ? scopeApplicationData(data, branch, await catalogForRequest()) : data;
}
export async function registerTestBranch(testId, { stream, branch } = {}) {
  if (typeof testId !== 'string' || !testId.trim() || testId.includes('$') || testId.includes('\0')) {
    throw Object.assign(new Error('A valid test ID is required.'), { statusCode: 400 });
  }
  const normalizedStream = String(stream || (/^(MMT|NCT|NMT|NEET)/i.test(testId) ? 'NEET' : 'JEE')).toUpperCase();
  const normalizedBranch = normalizedStream === 'NEET' ? null : String(branch || 'MAIN').toUpperCase();
  if (!['JEE', 'NEET'].includes(normalizedStream) || (normalizedStream === 'JEE' && !['MAIN', 'ADVANCED'].includes(normalizedBranch))) {
    throw Object.assign(new Error('Select a valid stream and JEE branch.'), { statusCode: 400 });
  }
  const previous = await TestBranch.findOne({ testId }).lean();
  if (previous && (previous.stream !== normalizedStream || previous.branch !== normalizedBranch)) {
    throw Object.assign(new Error(`Test ${testId} already belongs to ${previous.stream} ${previous.branch || ''}. Use a different test ID.`), { statusCode: 409 });
  }
  // Unlabelled existing JEE tests are Main. Do not silently reclassify historical data.
  if (!previous && normalizedBranch === 'ADVANCED') {
    const [raw, scores, topics] = await Promise.all([
      mongoose.connection.collection('studentrawmarks').findOne({ testId }),
      mongoose.connection.collection('testscores').findOne({ $or: [
        { [`tests.${testId.replace(/\./g, '___dot___')}`]: { $exists: true } },
        { $expr: { $gt: [{ $size: { $setIntersection: [
          { $map: { input: { $objectToArray: '$$ROOT' }, as: 'field', in: '$$field.k' } },
          [testId, ...['Physics','Chemistry','Math','Mathematics','PHY','CHE','MAT'].flatMap(subject => [`${testId}_${subject}`, `${subject} ${testId}`])],
        ] } }, 0] } },
      ] }),
      mongoose.connection.collection('topicmaps').findOne({ testId }),
    ]);
    if (raw || scores || topics) throw Object.assign(new Error(`Existing test ${testId} is Main. Use a new test ID for Advanced.`), { statusCode: 409 });
  }
  try {
    // Include immutable selection in the match: a concurrent conflicting upload
    // gets a unique-key conflict instead of silently reassigning the test.
    await TestBranch.updateOne({ testId, stream: normalizedStream, branch: normalizedBranch },
      { $setOnInsert: { testId, stream: normalizedStream, branch: normalizedBranch } }, { upsert: true });
  } catch (error) {
    if (error.code === 11000) throw Object.assign(new Error(`Test ${testId} was assigned to another stream or branch. Use a different test ID.`), { statusCode: 409 });
    throw error;
  }
}
export function scoreTestIds(scores) {
  return scores?.tests ? Object.keys(scores.tests) : Object.keys(flatToNested(scores || {}).tests).map(id => id.replace(/_(Attempted|Accuracy|Rank|Correct|Wrong)$/i, ''));
}
export async function registerScoreBranches(scores, selection) {
  for (const id of new Set(scoreTestIds(scores))) await registerTestBranch(id, selection);
}
export async function registerBulkScoreBranches(marks, selection) {
  const registrations = new Map();
  for (const mark of marks) {
    for (const id of scoreTestIds(mark.scores)) {
      const stream = selection.stream || mark.scores?.stream;
      const previous = registrations.get(id);
      if (previous?.stream && stream && previous.stream !== stream) {
        throw Object.assign(new Error(`Test ${id} has conflicting streams in this upload.`), { statusCode: 400 });
      }
      registrations.set(id, { ...selection, stream });
    }
  }
  for (const [id, metadata] of registrations) await registerTestBranch(id, metadata);
}
