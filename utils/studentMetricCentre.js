// Raw marks imports use sponsor aliases for these two centres.
export function sameStudentMetricCentre(left, right, stream) {
  const canonical = value => {
    const code = String(value ?? '').trim().toUpperCase();
    if (stream === 'NEET' && code === 'MUMM') return 'MUM';
    return ({ OIL_INDIA: 'JDH', 'OIL INDIA': 'JDH', GAIL: 'KNP' })[code] || code;
  };
  return Boolean(canonical(left)) && canonical(left) === canonical(right);
}
