// Explicit subject corrections shared by new calculations and saved results.
export function correctedTopicSubject(topic, testId) {
  const name = String(topic || '').split('/').pop().trim().replace(/\s+/g, ' ');
  if (String(testId || '').trim().toUpperCase() === 'NCT01' && /^biomolecules$/i.test(name)) return 'ZOOLOGY';
  if (/^ionic equ(?:i)?librium$/i.test(name)) return 'CHEMISTRY';
  if (/^basic maths?(?:\s*\([^)]*\))?$/i.test(name)
      || /^sets?\s*(?:&|and)\s*relations?$/i.test(name)) return 'MATHEMATICS';
  return null;
}

// Preserve classifications and percentages while correcting historical grouping.
export function normalizeTopicSubjects(doc) {
  if (!doc?.subjectWise) return doc;
  const subjectWise = Object.fromEntries(Object.entries(doc.subjectWise).map(([subject, groups]) => [subject,
    Object.fromEntries(Object.entries(groups).map(([level, items]) => [level, Array.isArray(items) ? [...items] : items]))
  ]));
  for (const level of ['strong', 'moderate', 'weak']) {
    const moved = [];
    for (const [subject, groups] of Object.entries(subjectWise)) {
      groups[level] = (groups[level] || []).filter(item => {
        const target = correctedTopicSubject(typeof item === 'string' ? item : item?.topic, doc.testId);
        if (!target || target === subject) return true;
        moved.push({ target, item });
        return false;
      });
    }
    for (const { target, item } of moved) {
      subjectWise[target] ||= {};
      subjectWise[target][level] ||= [];
      subjectWise[target][level].push(item);
    }
  }
  return { ...doc, subjectWise };
}

