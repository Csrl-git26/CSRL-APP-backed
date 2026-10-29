// Shared guard for rows merged into charts from question-wise uploads.
export function matchesTestStream(testId, stream = 'JEE') {
  const selected = String(stream || 'JEE').trim().toUpperCase();
  if (selected === 'ALL') return true;
  const isNeet = /^\s*(MMT|NCT|NMT|NRT|NEET)/i.test(String(testId || ''));
  return selected === 'NEET' ? isNeet : !isNeet;
}
