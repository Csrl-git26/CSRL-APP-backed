import sys

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx', 'r') as f:
    content = f.read()

start_idx = content.find("      {/* TWO COLUMNS */}")
end_idx = content.find("      {/* FULL WIDTH: Performance Graph */}")

if start_idx != -1 and end_idx != -1:
    before = content[:start_idx]
    after = content[end_idx:]
    
    # We want to extract just the Weak Subjects Analysis block
    weak_start = content.find("<div style={{ background: '#fff1f2'", start_idx)
    weak_end = content.find("</div>\n        </div>\n      </div>", weak_start) + len("</div>")
    
    weak_content = content[weak_start:weak_end]
    
    replacement = f"""      {{/* Weak Subjects Analysis */}}
      <div style={{{{ marginBottom: '12px' }}}}>
        {weak_content}
      </div>\n\n"""
      
    with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx', 'w') as f:
        f.write(before + replacement + after)
    print("Patched successfully")
else:
    print("Could not find boundaries")
