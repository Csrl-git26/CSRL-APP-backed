import sys

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx', 'r') as f:
    content = f.read()

bad_margin = "margin={{ top: 5, left: -25, bottom: -5, right: 10 }}"
good_margin = "margin={{ top: 5, left: 0, bottom: -5, right: 10 }}"

if bad_margin in content:
    content = content.replace(bad_margin, good_margin)
    with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx', 'w') as f:
        f.write(content)
    print("Patched graph left margin.")
else:
    print("Could not find bad_margin.")
