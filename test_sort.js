function sortTestRows(rows) {
  const parseSequence = (name) => {
    const match = name.match(/^([A-Za-z\-]+)(\d+)(.*)$/);
    if (!match) return null;
    return {
      prefix: match[1].toUpperCase().replace(/[^A-Z]/g, ''),
      num: parseInt(match[2], 10)
    };
  };

  const getLogicalIndex = (seq) => {
    if (!seq) return -1;
    if (seq.prefix === 'MT' || seq.prefix === 'PT') return seq.num * 10;
    if (seq.prefix === 'CMT' || seq.prefix === 'JCT') return seq.num * 20 + 5;
    if (seq.prefix === 'FMT') return 1000 + seq.num * 10;
    return -1;
  };

  return rows.sort((a, b) => {
    const seqA = parseSequence(a.name);
    const seqB = parseSequence(b.name);
    const idxA = getLogicalIndex(seqA);
    const idxB = getLogicalIndex(seqB);

    if (idxA !== -1 && idxB !== -1 && idxA !== idxB) {
      return idxA - idxB;
    }
    return a.name.localeCompare(b.name, undefined, { numeric: true });
  });
}

const tests = [
  { name: 'MT02' },
  { name: 'CMT01' },
  { name: 'MT01' },
  { name: 'MT03' },
  { name: 'CMT02' },
  { name: 'FMT01' },
  { name: 'MT04' }
];

console.log(sortTestRows(tests).map(t => t.name));
