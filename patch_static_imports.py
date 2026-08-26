import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad_imports = """        const { jsPDF } = await import('jspdf');
        const html2canvas = (await import('html2canvas')).default;"""
good_imports = """        // Using static imports to avoid dynamic import interop issues"""

top_bad = "import { LayoutDashboard"
top_good = "import { jsPDF } from 'jspdf';\nimport html2canvas from 'html2canvas';\nimport { LayoutDashboard"

if bad_imports in content:
    content = content.replace(bad_imports, good_imports)
    content = content.replace(top_bad, top_good)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched static imports successfully")
else:
    print("Could not find dynamic imports")
