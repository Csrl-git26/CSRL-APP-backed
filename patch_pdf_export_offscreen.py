import sys

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx', 'r') as f:
    content = f.read()

bad_div = "      <div style={{ position: 'absolute', left: '-9999px', top: '-9999px', opacity: 0, pointerEvents: 'none' }}>"
good_div = "      <div style={{ position: 'absolute', left: '0', top: '0', zIndex: -1000, opacity: 0, pointerEvents: 'none' }}>"

if bad_div in content:
    content = content.replace(bad_div, good_div)
    with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx', 'w') as f:
        f.write(content)
    print("Patched div successfully")
else:
    print("Could not find bad_div string in file.")
