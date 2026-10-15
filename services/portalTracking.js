// Server time is authoritative; a long network gap is not portal usage.
export const OFFLINE_AFTER_MS = 90_000;
export function advanceSession(session, now, active, end = false) {
  const elapsed = Math.max(0, now.getTime() - new Date(session.lastSeenAt).getTime());
  const connected = elapsed <= OFFLINE_AFTER_MS ? elapsed : 0;
  const previouslyActive = Math.max(0, new Date(session.activeUntil || 0).getTime() - new Date(session.lastSeenAt).getTime());
  return {
    lastSeenAt: now,
    sessionMs: (session.sessionMs || 0) + connected,
    activeMs: (session.activeMs || 0) + Math.min(connected, previouslyActive),
    // A short activity lease lets multiple tabs share a session without double counting.
    activeUntil: end ? now : new Date(Math.max(new Date(session.activeUntil || 0).getTime(), active ? now.getTime() + 35_000 : 0)),
    ...(end ? { endedAt: now } : {}),
    revision: session.revision + 1,
  };
}
export function publicSession(s, now = Date.now()) {
  const status = s.endedAt ? 'Logged out' : now - new Date(s.lastSeenAt).getTime() <= OFFLINE_AFTER_MS ? 'Online' : 'Offline';
  const { activeUntil, revision, ...row } = s;
  return { ...row, status, endIsEstimated: status === 'Offline', endTime: s.endedAt || (status === 'Offline' ? s.lastSeenAt : null) };
}
