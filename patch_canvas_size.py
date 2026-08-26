import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad = """          const imgData = canvas.toDataURL('image/jpeg', 1.0);
          const pdfWidth = 210;
          const pdfHeight = (canvas.height * pdfWidth) / canvas.width;"""

good = """          if (canvas.width === 0 || canvas.height === 0) {
            throw new Error(`Canvas is 0x0 for student ${rollKey}. Element might be hidden.`);
          }
          const imgData = canvas.toDataURL('image/jpeg', 1.0);
          const pdfWidth = 210;
          const pdfHeight = (canvas.height * pdfWidth) / canvas.width;"""

if bad in content:
    content = content.replace(bad, good)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched canvas size guard successfully")
else:
    print("Could not find canvas size block")
