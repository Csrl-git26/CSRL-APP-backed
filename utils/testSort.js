export function getTestLogicalIndex(name) {
  if (!name) return -1;
  const match = String(name).match(/^([A-Za-z\-]+)(\d+)(.*)$/);
  if (!match) return -1;
  
  const prefix = match[1].replace(/[^A-Za-z]/g, '').toUpperCase();
  const num = parseInt(match[2], 10);
  
  if (['MT', 'PT', 'NMT', 'MMT'].includes(prefix)) {
    return num * 10;
  }
  if (['CMT', 'JCT', 'NCT', 'MCT'].includes(prefix)) {
    return num * 20 + 5;
  }
  if (['FMT', 'NFT', 'MFT'].includes(prefix)) {
    return 1000 + num * 10;
  }
  return -1;
}

export function compareTestsAsc(a, b) {
  const nameA = String(a || '');
  const nameB = String(b || '');
  const idxA = getTestLogicalIndex(nameA);
  const idxB = getTestLogicalIndex(nameB);
  
  if (idxA !== -1 && idxB !== -1) {
    if (idxA !== idxB) return idxA - idxB;
  } else if (idxA !== -1) {
    return -1;
  } else if (idxB !== -1) {
    return 1;
  }
  return nameA.localeCompare(nameB, undefined, { numeric: true, sensitivity: 'base' });
}

export function compareTestsDesc(a, b) {
  return compareTestsAsc(b, a);
}
