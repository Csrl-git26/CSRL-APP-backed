import sys

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx', 'r') as f:
    content = f.read()

weak_start_marker = "      {/* FULL WIDTH: Overall Weak Topics */}"
perf_start_marker = "      <h3 style={{ fontSize: '14px', fontWeight: 800, color: '#0f172a', textTransform: 'uppercase', marginBottom: '12px', borderBottom: '1px solid #cbd5e1', paddingBottom: '4px' }}>\n        Performance Test Records\n      </h3>"
perf_end_marker = "        * Reference: M = Marks, AT. = Attempted Questions, AC. = Accuracy %\n      </div>"

weak_start_idx = content.find(weak_start_marker)
perf_start_idx = content.find(perf_start_marker)
perf_end_idx = content.find(perf_end_marker) + len(perf_end_marker)

if weak_start_idx != -1 and perf_start_idx != -1 and perf_end_idx != -1:
    weak_block = content[weak_start_idx:perf_start_idx].strip()
    perf_block = content[perf_start_idx:perf_end_idx].strip()
    
    before = content[:weak_start_idx]
    after = content[perf_end_idx:]
    
    new_content = before + perf_block + "\n\n      " + weak_block + "\n" + after
    
    with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx', 'w') as f:
        f.write(new_content)
    print("Swapped successfully")
else:
    print(f"Failed to find markers: weak={weak_start_idx}, perf_start={perf_start_idx}, perf_end={perf_end_idx}")
