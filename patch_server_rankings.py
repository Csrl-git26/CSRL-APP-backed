import sys

filepath = '/Users/surya/Desktop/CSRL-APP-backed/server.js'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """  if (order === 'asc') ranked = ranked.filter(s => s.marks !== 'Absent').reverse();

  const n = Math.min(parseInt(limit, 10) || 30, ranked.length);
  res.json({
    ranked: ranked.slice(0, n),
    total: ranked.length,
    absentCount: absent,
    testKey,
  });"""

new_block = """  if (order === 'asc') ranked = ranked.filter(s => s.marks !== 'Absent').reverse();

  const n = Math.min(parseInt(limit, 10) || 30, ranked.length);
  const sliced = ranked.slice(0, n);

  // Compute ranks for all FMT tests to display as extra columns
  const fmtKeysList = Array.from(new Set(source.testColumns.filter(k => k.startsWith('FMT')).map(k => k.split('_')[0])));
  const fmtRanksMap = {};
  
  for (const fk of fmtKeysList) {
    const fkRanked = rankStudentsByTest(source.profiles, source.tests, fk);
    fkRanked.forEach(st => {
      if (!fmtRanksMap[st.roll]) fmtRanksMap[st.roll] = {};
      if (st.rank && st.rank !== '-') fmtRanksMap[st.roll][fk] = st.rank;
    });
  }

  const finalRanked = sliced.map(st => ({
     ...st,
     fmtRanks: fmtRanksMap[st.roll] || {}
  }));

  res.json({
    ranked: finalRanked,
    total: ranked.length,
    absentCount: absent,
    testKey,
  });"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched server.js successfully!")
else:
    print("Could not find old_block in server.js")
