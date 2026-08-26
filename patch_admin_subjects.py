import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_mapping = """                {allSubjects.map((sub) => (
                  <td key={sub} style={{ color: flatM.subjects[sub] === undefined ? 'var(--gray-200)' : 'inherit' }}>
                    {flatM.subjects[sub] ?? '—'}
                  </td>
                ))}"""

new_mapping = """                {allSubjects.map((sub) => {
                  let val = flatM.subjects[sub];
                  if (val === undefined && m.rawScores) {
                    val = m.rawScores[`${selectedTestKey}_${sub}`];
                    if (val === undefined) {
                      val = m.rawScores[sub];
                    }
                  }
                  return (
                    <td key={sub} style={{ color: val === undefined ? 'var(--gray-200)' : 'inherit' }}>
                      {val ?? '—'}
                    </td>
                  );
                })}"""

if old_mapping in content:
    content = content.replace(old_mapping, new_mapping)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched AdminDashboard.jsx successfully!")
else:
    print("Failed to find old block in AdminDashboard.jsx")
