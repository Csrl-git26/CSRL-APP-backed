// Correct historical saved classification on read, preserving all rates and marks.
export function normalizeTopicSubjects(doc) {
  if (!doc?.subjectWise) return doc;
  const isIonic = item => /^ionic equ(?:i)?librium$/i.test(String(typeof item === 'string' ? item : item?.topic).trim());
  const subjectWise = Object.fromEntries(Object.entries(doc.subjectWise).map(([subject, groups]) => [subject, { ...groups }]));
  subjectWise.CHEMISTRY ||= {};
  for (const level of ['strong', 'moderate', 'weak']) {
    const moved = [];
    for (const [subject, groups] of Object.entries(subjectWise)) {
      if (subject === 'CHEMISTRY') continue;
      moved.push(...(groups[level] || []).filter(isIonic));
      groups[level] = (groups[level] || []).filter(item => !isIonic(item));
    }
    subjectWise.CHEMISTRY[level] = [...(subjectWise.CHEMISTRY[level] || []), ...moved];
  }
  return { ...doc, subjectWise };
}
