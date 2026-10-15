import fs from 'node:fs';
import { randomUUID, scrypt, timingSafeEqual } from 'node:crypto';
import { promisify } from 'node:util';
import PortalUser from '../models/PortalUser.js';
import { ADMIN_CREDENTIALS } from '../config/centers.js';
const deriveKey = promisify(scrypt);
const directories = Object.fromEntries([['centre', 'centre'], ['admin', 'management']].map(([role, file]) => {
  const directory = JSON.parse(fs.readFileSync(new URL(`../config/${file}Users.json`, import.meta.url)));
  return [role, { ...directory, byId: new Map(directory.users.map(u => [u.id, u])) }];
}));
const normalize = value => String(value || '').trim().toLowerCase();
const reserved = new Set(['admin', 'centre', 'bog', normalize(ADMIN_CREDENTIALS.username)]);
const key = (role, id) => `${role}:${id}`;
export function userError(status, message) { return Object.assign(new Error(message), { status }); }
function checkRole(role) { if (!Object.hasOwn(directories, role)) throw userError(400, 'Choose Centre or CSRL Management login.'); }
const publicUser = (role, user) => ({ role, userId: user.userId || user.id, name: user.name, centres: user.centres || [], version: user.version || 'baseline' });

export function createPortalUserService(Model = PortalUser) {
  async function getUser(role, id) {
    checkRole(role);
    const userId = normalize(id);
    const override = await Model.findById(key(role, userId)).lean();
    if (override) return override.disabled ? null : publicUser(role, override);
    const original = directories[role].byId.get(userId);
    return original ? publicUser(role, original) : null;
  }
  return {
    async authenticate(role, id, password) {
      checkRole(role);
      if (reserved.has(normalize(id)) || typeof password !== 'string' || password.length > 256) return null;
      const user = await getUser(role, id);
      if (!user) return null;
      const directory = directories[role];
      const hash = await deriveKey(password, directory.passwordSalt, 64);
      return timingSafeEqual(hash, Buffer.from(directory.passwordHash, 'hex')) ? { ...user, id: user.userId } : null;
    },
    async isTokenActive(user) {
      if (!['centre', 'admin'].includes(user.role) || !user.loginUserId) return true;
      const account = await getUser(user.role, user.loginUserId);
      return !!account && account.version === (user.accountVersion || 'baseline');
    },
    async list(role) {
      checkRole(role);
      const merged = new Map(directories[role].users.map(u => [u.id, publicUser(role, u)]));
      const overrides = await Model.find({ role }).lean();
      for (const u of overrides) {
        if (u.disabled) merged.delete(u.userId);
        else merged.set(u.userId, publicUser(role, u));
      }
      return [...merged.values()].sort((a, b) => a.name.localeCompare(b.name) || a.userId.localeCompare(b.userId));
    },
    async add(role, input, actor) {
      checkRole(role);
      const userId = normalize(input.userId);
      const name = String(input.name || '').trim();
      if (!/^[a-z0-9][a-z0-9._@+\-]{1,119}$/.test(userId)) throw userError(400, 'User ID must be 2–120 characters using letters, numbers, dots, @, +, - or _.');
      if (reserved.has(userId)) throw userError(400, 'This user ID is reserved for an existing system login.');
      if (!name || name.length > 120) throw userError(400, 'Enter a name of up to 120 characters.');
      if (!Array.isArray(input.centres) || input.centres.length > 20 || input.centres.some(c => typeof c !== 'string' || c.length > 80)) throw userError(400, 'Enter valid centre or office names.');
      const centres = [...new Set(input.centres.map(c => c.trim().toUpperCase()).filter(Boolean))];
      const existing = await Model.findById(key(role, userId)).lean();
      if (existing ? !existing.disabled : directories[role].byId.has(userId)) throw userError(409, 'This user ID already exists for this login page.');
      const record = { _id: key(role, userId), role, userId, name, centres, disabled: false, version: randomUUID(), changedBy: actor };
      try {
        if (existing) {
          const { _id, ...updates } = record;
          const updated = await Model.findOneAndUpdate({ _id, version: existing.version, disabled: true }, { $set: updates }, { new: true }).lean();
          if (!updated) throw userError(409, 'This user changed. Refresh the list and try again.');
        } else await Model.create(record);
      } catch (e) {
        if (e.code === 11000) throw userError(409, 'This user ID was just added. Refresh the list.');
        throw e;
      }
      return publicUser(role, record);
    },
    async remove(role, id, version, actor) {
      checkRole(role);
      const userId = normalize(id);
      const existing = await Model.findById(key(role, userId)).lean();
      const original = directories[role].byId.get(userId);
      if (existing?.disabled || (!existing && !original)) throw userError(404, 'User ID is no longer available. Refresh the list.');
      if (version !== (existing?.version || 'baseline')) throw userError(409, 'This user changed. Refresh the list before deleting.');
      try {
        if (existing) {
          const result = await Model.findOneAndUpdate({ _id: existing._id, version, disabled: false }, { $set: { disabled: true, version: randomUUID(), changedBy: actor } }, { new: true }).lean();
          if (!result) throw userError(409, 'This user changed. Refresh the list before deleting.');
        } else {
          await Model.create({ _id: key(role, userId), role, userId, name: original.name, centres: original.centres, disabled: true, version: randomUUID(), changedBy: actor });
        }
      } catch (e) {
        if (e.code === 11000) throw userError(409, 'This user changed. Refresh the list before deleting.');
        throw e;
      }
    },
  };
}
export const portalUsers = createPortalUserService();
