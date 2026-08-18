import NodeCache from 'node-cache';
import Redis from 'ioredis';
import { isMongoReady, initMongo } from './mongoInit.js';
import Profile from '../models/Profile.js';
import TestScore from '../models/TestScore.js';
import { flatToNested, nestedToFlat, extractColumnsFromNestedTests } from '../utils/testColumns.js';

const GLOBAL_DATA_CACHE_KEY = 'globalData';
const pendingGlobalQueries = new Map();

function readCacheTtlMs() {
  const raw = process.env.DB_READ_CACHE_TTL_MS || process.env.FIRESTORE_READ_CACHE_TTL_MS;
  if (raw === '0' || raw === '') return 0;
  const n = parseInt(raw ?? '3600000', 10);
  return Number.isFinite(n) && n >= 0 ? n : 3600000;
}

function readCacheTtlSeconds() {
  const ms = readCacheTtlMs();
  return ms <= 0 ? 0 : Math.max(1, Math.floor(ms / 1000));
}

const ttlSec = readCacheTtlSeconds() || 10;
const globalDataCache = new NodeCache({
  stdTTL: ttlSec,
  checkperiod: Math.min(120, Math.max(5, Math.floor(ttlSec / 2))),
  useClones: true,
});

let redisClient = null;
if (process.env.REDIS_URL) {
  try {
    let url = process.env.REDIS_URL;
    // Auto-fix if the user accidentally pasted the Upstash CLI command instead of just the URL
    if (url.includes('--tls -u ')) {
      url = url.split('--tls -u ')[1].trim();
    }
    
    // Enforce TLS for Upstash/managed Redis by ensuring protocol is rediss://
    if (url.startsWith('redis://') && url.includes('upstash.io')) {
      url = url.replace('redis://', 'rediss://');
    }
    
    redisClient = new Redis(url, {
      tls: url.startsWith('rediss://') ? { rejectUnauthorized: false } : undefined,
      retryStrategy(times) {
        return Math.min(times * 50, 2000); // Reconnect after 50ms, max 2s
      },
      maxRetriesPerRequest: null,
    });
    
    redisClient.on('error', (err) => {
      // Suppress ECONNRESET logs to prevent log spam when idle connections drop
      if (err.code !== 'ECONNRESET') {
        console.error('[Redis] Error:', err);
      }
    });
  } catch (err) {
    console.error('[Redis] Failed to initialize Redis client. Falling back to NodeCache. Error:', err.message);
    redisClient = null;
  }
}

async function getCacheAsync(key) {
  if (redisClient) {
    try {
      const data = await redisClient.get(key);
      if (data) return JSON.parse(data);
    } catch (err) {
      console.error('[Redis] GET error for key', key, ':', err);
    }
  }
  return globalDataCache.get(key);
}

async function setCacheAsync(key, value, ttlSeconds) {
  if (redisClient) {
    try {
      if (ttlSeconds > 0) {
        await redisClient.set(key, JSON.stringify(value), 'EX', ttlSeconds);
      } else {
        await redisClient.set(key, JSON.stringify(value));
      }
      return;
    } catch (err) {
      console.error('[Redis] SET error for key', key, ':', err);
    }
  }
  globalDataCache.set(key, value);
}

export function invalidateDataCache() {
  globalDataCache.flushAll();
  if (redisClient) {
    redisClient.flushdb().catch(err => console.error('[Redis] flushdb error:', err));
  }
}

// Keep the same export name as the old one so server.js doesn't break if anything still imports it
export const invalidateFirestoreReadCache = invalidateDataCache;

export function getReadCacheStatus() {
  const ttlMs = readCacheTtlMs();
  return {
    backend: redisClient ? 'redis' : 'node-cache',
    ttlMs,
    ttlSeconds: ttlMs > 0 ? ttlSec : 0,
    enabled: ttlMs > 0,
    key: GLOBAL_DATA_CACHE_KEY,
  };
}

export function isDbEnabled() {
  // Try to init, and it returns true if URI exists
  initMongo();
  return process.env.MONGODB_URI !== undefined;
}

export const isFirestoreEnabled = isDbEnabled;

function stripUndefined(obj) {
  const out = {};
  for (const [k, v] of Object.entries(obj)) {
    if (v !== undefined) out[k] = v;
  }
  return out;
}

// MongoDB does not allow dots in field names (treats them as path separators).
// We encode dots as '___dot___' on write and restore them on read.
function sanitizeKeysForMongo(obj) {
  const out = {};
  for (const [k, v] of Object.entries(obj)) {
    const safeKey = k.replace(/\./g, '___dot___');
    out[safeKey] = v;
  }
  return out;
}

function restoreKeysFromMongo(obj) {
  const out = {};
  for (const [k, v] of Object.entries(obj)) {
    const origKey = k.replace(/___dot___/g, '.');
    out[origKey] = v;
  }
  return out;
}

function isNestedFormat(doc) {
  return doc && typeof doc.tests === 'object' && doc.tests !== null;
}

function ensureNested(rawDoc) {
  if (!rawDoc) return rawDoc;
  if (isNestedFormat(rawDoc)) {
    const normalized = {
      ...rawDoc,
      ROLL_KEY: rawDoc.ROLL_KEY || rawDoc.rollKey || '',
      centerCode: rawDoc.centerCode || rawDoc.centreCode || '',
      tests: {},
    };

    for (const [testName, testData] of Object.entries(rawDoc.tests || {})) {
      if (!testData || typeof testData !== 'object') continue;
      const one = { ...testData };
      if (one.total === undefined && one.Total !== undefined) one.total = one.Total;
      delete one.Total;
      normalized.tests[testName] = one;
    }

    return normalized;
  }
  return flatToNested(rawDoc);
}

let memoryDevStore = null;

function getMemoryDevStore() {
  if (!memoryDevStore) {
    memoryDevStore = { profiles: [], tests: [], testColumns: [] };
  }
  return memoryDevStore;
}

export async function loadApplicationData() {
  if (!isDbEnabled()) {
    return getMemoryDevStore();
  }
  return loadGlobalDataFromDb();
}

export async function loadCenterApplicationData(centerCode) {
  if (!isDbEnabled()) {
    return sliceCenterFromGlobal(getMemoryDevStore(), centerCode);
  }
  return loadCenterDataFromDb(centerCode);
}

function normalizeCenterCode(v) {
  return String(v ?? '').trim().toUpperCase();
}

export function sliceCenterFromGlobal(globalData, centerCode) {
  const normCenter = normalizeCenterCode(centerCode);
  const profiles = globalData.profiles.filter((p) => normalizeCenterCode(p.centerCode) === normCenter);
  
  const rollSet = new Set(profiles.map(p => p.ROLL_KEY));
  const tests = globalData.tests.filter((t) => rollSet.has(t.ROLL_KEY));
  const colSet = new Set();
  tests.forEach((t) => {
    Object.keys(t).forEach((k) => {
      // Ignore meta keys
      if (k === 'ROLL_KEY' || k === 'centerCode' || k === 'stream' || k === '_id' || k === '__v' || k === 'createdAt' || k === 'updatedAt') return;
      // Ignore ghost test names and redundant data
      if (k.length <= 1 || k === 'NAME' || k === 'centreCode' || k === 'CAT4' || k.startsWith('CAT4_')) return;
      
      colSet.add(k);
    });
  });
  const testColumns = colSet.size > 0 ? Array.from(colSet) : globalData.testColumns;
  return { profiles, tests, testColumns };
}

function processDbDocuments(profilesDocs, tDocs) {
  const pDocs = profilesDocs.map(d => {
    // Restore any dot-encoded keys (___dot___ -> .) stored to work around MongoDB restrictions
    const obj = restoreKeysFromMongo({ ...d });
    delete obj._id;
    delete obj.__v;
    delete obj.createdAt;
    delete obj.updatedAt;

    // Find keys dynamically to handle casing differences like "Mobile No" vs "MOBILE NO"
    const keys = Object.keys(obj);
    
    const mobileKey = keys.find(k => k.toLowerCase() === 'mobile no');
    if (mobileKey) {
      obj['Mobile No.'] = obj[mobileKey];
      delete obj[mobileKey];
    }
    
    // Also inject a standard "Mobile" key just in case the frontend relies on that
    if (obj['Mobile No.']) obj['Mobile'] = obj['Mobile No.'];

    const rollNoKey = keys.find(k => k.toLowerCase() === 'roll no');
    if (rollNoKey) {
      obj['ROLL NO.'] = obj[rollNoKey];
      delete obj[rollNoKey];
    }

    const fatherMobileKey = keys.find(k => k.toLowerCase() === 'fathers mobile');
    if (fatherMobileKey) {
      obj["FATHER'S MOBILE"] = obj[fatherMobileKey];
    }

    const fatherMobileNoKey = keys.find(k => k.toLowerCase() === 'fathers mobile no');
    if (fatherMobileNoKey) {
      obj["FATHER'S MOBILE NO."] = obj[fatherMobileNoKey];
    }

    return obj;
  });

  const testColumnsSet = new Set();
  const tests = tDocs.map((d) => {
    const raw = { ...d };
    delete raw._id;
    delete raw.__v;
    delete raw.createdAt;
    delete raw.updatedAt;
    
    const nested = ensureNested(raw);
    const flat = nestedToFlat(nested);
    extractColumnsFromNestedTests(nested.tests).forEach((c) => testColumnsSet.add(c));
    return flat;
  });

  return {
    profiles: pDocs,
    tests,
    testColumns: Array.from(testColumnsSet),
  };
}

async function fetchGlobalDataFromDbOnce() {
  await initMongo();
  
  const [profilesDocs, tDocs] = await Promise.all([
    Profile.find({}).lean(),
    TestScore.find({}).lean()
  ]);

  return processDbDocuments(profilesDocs, tDocs);
}

async function fetchCenterDataFromDbOnce(centerCode) {
  await initMongo();
  const normCenter = normalizeCenterCode(centerCode);
  
  const profilesDocs = await Profile.find({ centerCode: new RegExp(`^${normCenter}$`, 'i') }).lean();
  
  // Get all ROLL_KEYs for this centre to fetch their tests
  const rollKeys = profilesDocs.map(p => p.ROLL_KEY);
  
  const tDocs = await TestScore.find({ ROLL_KEY: { $in: rollKeys } }).lean();

  return processDbDocuments(profilesDocs, tDocs);
}

export async function loadGlobalDataFromDb() {
  if (!isDbEnabled()) {
    return { profiles: [], tests: [], testColumns: [] };
  }

  if (pendingGlobalQueries.has(GLOBAL_DATA_CACHE_KEY)) {
    return pendingGlobalQueries.get(GLOBAL_DATA_CACHE_KEY);
  }

  const promise = (async () => {
    const ttlMs = readCacheTtlMs();
    const ttlSec = readCacheTtlSeconds();

    if (ttlMs > 0) {
      const cached = await getCacheAsync(GLOBAL_DATA_CACHE_KEY);
      if (cached) {
        return {
          profiles: cached.profiles ?? [],
          tests: cached.tests ?? [],
          testColumns: cached.testColumns ?? [],
        };
      }
    }

    try {
      const data = await fetchGlobalDataFromDbOnce();
      const out = {
        profiles: data.profiles,
        tests: data.tests,
        testColumns: data.testColumns,
      };
      if (ttlMs > 0) {
        await setCacheAsync(GLOBAL_DATA_CACHE_KEY, {
          profiles: out.profiles,
          tests: out.tests,
          testColumns: out.testColumns,
        }, ttlSec);
      }
      return out;
    } catch (err) {
      console.error('Error in loadGlobalDataFromDb:', err);
      return { profiles: [], tests: [], testColumns: [] };
    } finally {
      pendingGlobalQueries.delete(GLOBAL_DATA_CACHE_KEY);
    }
  })();

  pendingGlobalQueries.set(GLOBAL_DATA_CACHE_KEY, promise);
  return promise;
}

export async function loadCenterDataFromDb(centerCode) {
  if (!isDbEnabled()) {
    return { profiles: [], tests: [], testColumns: [] };
  }

  const normCenter = normalizeCenterCode(centerCode);
  const cacheKey = `centerData_${normCenter}`;
  
  if (pendingGlobalQueries.has(cacheKey)) {
    return pendingGlobalQueries.get(cacheKey);
  }

  const promise = (async () => {
    const ttlMs = readCacheTtlMs();
    const ttlSec = readCacheTtlSeconds();

    if (ttlMs > 0) {
      const cached = await getCacheAsync(cacheKey);
      if (cached) {
        return {
          profiles: cached.profiles ?? [],
          tests: cached.tests ?? [],
          testColumns: cached.testColumns ?? [],
        };
      }
    }

    try {
      const data = await fetchCenterDataFromDbOnce(normCenter);
      const out = {
        profiles: data.profiles,
        tests: data.tests,
        testColumns: data.testColumns,
      };
      if (ttlMs > 0) {
        await setCacheAsync(cacheKey, {
          profiles: out.profiles,
          tests: out.tests,
          testColumns: out.testColumns,
        }, ttlSec);
      }
      return out;
    } catch (err) {
      console.error(`Error in loadCenterDataFromDb for ${centerCode}:`, err);
      return { profiles: [], tests: [], testColumns: [] };
    } finally {
      pendingGlobalQueries.delete(cacheKey);
    }
  })();

  pendingGlobalQueries.set(cacheKey, promise);
  return promise;
}

export async function upsertProfileDoc(student) {
  if (!isDbEnabled()) return;
  const { centerCode, ROLL_KEY } = student;
  if (!centerCode || !ROLL_KEY) throw new Error('centerCode and ROLL_KEY are required');

  await initMongo();
  // Sanitize field names: MongoDB forbids dots in field names used with $set
  const cleanStudent = sanitizeKeysForMongo(stripUndefined(student));
  
  await Profile.findOneAndUpdate(
    { centerCode, ROLL_KEY },
    { $set: cleanStudent },
    { upsert: true, new: true, setDefaultsOnInsert: true }
  );

  invalidateDataCache();
}

export async function deleteStudentDocs(centerCode, rollKey) {
  if (!isDbEnabled()) return;
  await initMongo();
  
  await Promise.all([
    Profile.deleteOne({ centerCode, ROLL_KEY: rollKey }),
    TestScore.deleteOne({ centerCode, ROLL_KEY: rollKey })
  ]);
  
  invalidateDataCache();
}

export async function upsertTestDoc(centerCode, rollKey, scores) {
  if (!isDbEnabled()) return {};

  await initMongo();

  const doc = await TestScore.findOne({ centerCode, ROLL_KEY: rollKey });
  let base;
  
  if (doc) {
    base = ensureNested(doc.toObject());
  } else {
    base = { ROLL_KEY: rollKey, centerCode, stream: 'JEE', tests: {} };
  }

  if (scores && typeof scores.tests === 'object') {
    for (const [testName, testData] of Object.entries(scores.tests)) {
      if (!base.tests[testName]) base.tests[testName] = {};
      Object.assign(base.tests[testName], testData);
    }
  } else {
    const patchNested = flatToNested({ ROLL_KEY: rollKey, centerCode, ...scores });
    for (const [testName, testData] of Object.entries(patchNested.tests)) {
      if (!base.tests[testName]) base.tests[testName] = {};
      Object.assign(base.tests[testName], testData);
    }
  }

  if (scores.stream) base.stream = scores.stream;

  const cleanBase = stripUndefined(base);
  
  await TestScore.findOneAndUpdate(
    { centerCode, ROLL_KEY: rollKey },
    { $set: cleanBase },
    { upsert: true, setDefaultsOnInsert: true }
  );

  invalidateDataCache();
  return nestedToFlat(base);
}

export async function loadSingleStudentDataFromDb(centerCode, rollKey) {
  if (!isDbEnabled()) {
    const mem = sliceCenterFromGlobal(getMemoryDevStore(), centerCode);
    return {
      profiles: mem.profiles.filter(p => p.ROLL_KEY === rollKey),
      tests: mem.tests.filter(t => t.ROLL_KEY === rollKey),
      testColumns: mem.testColumns
    };
  }

  await initMongo();
  const normCenter = normalizeCenterCode(centerCode);

  const [profileDoc, testDoc] = await Promise.all([
    Profile.findOne({ centerCode: new RegExp(`^${normCenter}$`, 'i'), ROLL_KEY: rollKey }).lean(),
    TestScore.findOne({ centerCode: new RegExp(`^${normCenter}$`, 'i'), ROLL_KEY: rollKey }).lean()
  ]);

  const pDocs = profileDoc ? [profileDoc] : [];
  const tDocs = testDoc ? [testDoc] : [];
  
  const processed = processDbDocuments(pDocs, tDocs);
  
  // We still need the global testColumns so charts render properly
  const centerData = await loadCenterDataFromDb(centerCode);
  
  return {
    profiles: processed.profiles,
    tests: processed.tests,
    testColumns: centerData.testColumns
  };
}
