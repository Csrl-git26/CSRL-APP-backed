import sys

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx', 'r') as f:
    content = f.read()

# 1. Update headers
old_header_subj = "M | AT. | AC.</div>"
new_header_subj = "M | AT. | AC. | Rk.</div>"
content = content.replace(old_header_subj, new_header_subj)

old_ref = "* Reference: M = Marks, AT. = Attempted Questions, AC. = Accuracy %"
new_ref = "* Reference: M = Marks, AT. = Attempted Questions, AC. = Accuracy %, Rk. = Rank"
content = content.replace(old_ref, new_ref)

# 2. Update renderCell
old_render = """            const renderCell = (v) => {
              const isAbsent = v.mark === 'A' || v.mark === 'a' || v.mark === 'Absent';
              if (isAbsent) return 'Absent';
              if (v.mark === null || v.mark === undefined || v.mark === '—') {
                if (v.attempted != null) return `— | ${v.attempted} | ${v.accuracy}%`;
                return '—';
              }
              const m = v.mark;
              const at = v.attempted != null ? v.attempted : '—';
              const ac = v.accuracy != null ? `${v.accuracy}%` : '—';
              return `${m} | ${at} | ${ac}`;
            };"""

new_render = """            const renderCell = (v) => {
              const isAbsent = v.mark === 'A' || v.mark === 'a' || v.mark === 'Absent';
              if (isAbsent) return 'Absent';
              if (v.mark === null || v.mark === undefined || v.mark === '—') {
                if (v.attempted != null) return `— | ${v.attempted} | ${v.accuracy}% | ${v.rank || '—'}`;
                return '—';
              }
              const m = v.mark;
              const at = v.attempted != null ? v.attempted : '—';
              const ac = v.accuracy != null ? `${v.accuracy}%` : '—';
              const rk = v.rank != null ? v.rank : '—';
              return `${m} | ${at} | ${ac} | ${rk}`;
            };"""

content = content.replace(old_render, new_render)

# 3. Update subjects map
old_sub = """                  const mark = row[s];
                  const attempted = row[`${s}_Attempted`];
                  const accuracy = row[`${s}_Accuracy`];
                  const v = { mark, attempted, accuracy };"""

new_sub = """                  const mark = row[s];
                  const attempted = row[`${s}_Attempted`];
                  const accuracy = row[`${s}_Accuracy`];
                  const rank = row[`${s}_Rank`];
                  const v = { mark, attempted, accuracy, rank };"""

content = content.replace(old_sub, new_sub)

# 4. Update Total
old_tot = "{renderCell({ mark: row.Total, attempted: row.Total_Attempted, accuracy: row.Total_Accuracy })}"
new_tot = "{renderCell({ mark: row.Total, attempted: row.Total_Attempted, accuracy: row.Total_Accuracy, rank: row.Total_Rank })}"
content = content.replace(old_tot, new_tot)


with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx', 'w') as f:
    f.write(content)

print("Patched table successfully.")
