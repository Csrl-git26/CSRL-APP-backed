import fs from 'node:fs';
import { scryptSync, timingSafeEqual } from 'node:crypto';
const directory = JSON.parse(fs.readFileSync(new URL('../config/centreUsers.json', import.meta.url), 'utf8'));
const users = new Map(directory.users.map(user => [user.id, user]));
export function authenticateCentreUser(id, password) {
  const user = users.get(String(id || '').trim().toLowerCase());
  if (!user || typeof password !== 'string' || password.length > 256) return null;
  const hash = scryptSync(password, directory.passwordSalt, 64);
  return timingSafeEqual(hash, Buffer.from(directory.passwordHash, 'hex')) ? user : null;
}
