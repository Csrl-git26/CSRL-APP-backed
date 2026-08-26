import sys

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx', 'r') as f:
    content = f.read()

bad_h2c = """        const canvas1 = await html2canvas(page1, { 
          scale: 2, 
          useCORS: true,
          windowHeight: page1.scrollHeight
        });"""

good_h2c = """        const canvas1 = await html2canvas(page1, { 
          scale: 2, 
          useCORS: true,
          windowHeight: page1.scrollHeight,
          height: page1.scrollHeight,
          windowWidth: 800,
          width: 800
        });"""

if bad_h2c in content:
    content = content.replace(bad_h2c, good_h2c)
    with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx', 'w') as f:
        f.write(content)
    print("Patched html2canvas successfully")
else:
    print("Could not find bad_h2c string in file.")
