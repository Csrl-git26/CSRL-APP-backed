filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """    // Average Marks
    const minAvg = Math.min(...subjectAvgs.map((s) => s.avg));
    const tiedAvg = subjectAvgs.filter((s) => s.avg === minAvg);
    const labelAvg = tiedAvg.length === 1
      ? `${tiedAvg[0].subject} (${minAvg}/${streamCfg.maxBySubject?.[tiedAvg[0].subject] || 100})`
      : `${tiedAvg.map((t) => t.subject).join(', ')} (${minAvg}/${streamCfg.maxBySubject?.[tiedAvg[0].subject] || 100})`;
      
    return { minSubjectAvg: minAvg, weakSubjectFromPerformance: labelAvg };"""

new_block = """    // Average Marks — filter out non-numeric avgs to prevent NaN crash
    const validAvgs = subjectAvgs.filter((s) => typeof s.avg === 'number' && Number.isFinite(s.avg));
    if (!validAvgs.length) return { minSubjectAvg: null, weakSubjectFromPerformance: null };
    
    const minAvg = Math.min(...validAvgs.map((s) => s.avg));
    const tiedAvg = validAvgs.filter((s) => s.avg === minAvg);
    if (!tiedAvg.length) return { minSubjectAvg: null, weakSubjectFromPerformance: null };
    
    const labelAvg = tiedAvg.length === 1
      ? `${tiedAvg[0].subject} (${minAvg}/${streamCfg.maxBySubject?.[tiedAvg[0].subject] || 100})`
      : `${tiedAvg.map((t) => t.subject).join(', ')} (${minAvg}/${streamCfg.maxBySubject?.[tiedAvg[0].subject] || 100})`;
      
    return { minSubjectAvg: minAvg, weakSubjectFromPerformance: labelAvg };"""

if old_block in content:
    content = content.replace(old_block, new_block)
    print("Fixed: NaN-safe minAvg calculation")
else:
    print("ERROR: Could not find the block to replace!")
    # Show what we have
    idx = content.find("const minAvg = Math.min")
    if idx >= 0:
        print("Found minAvg at:", content[idx-20:idx+200])

with open(filepath, 'w') as f:
    f.write(content)
