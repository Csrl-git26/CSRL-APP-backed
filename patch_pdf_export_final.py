import sys

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx', 'r') as f:
    lines = f.readlines()

new_func_lines = [
    "  const exportProfileToPDF = async () => {\n",
    "    if (!profile) return;\n",
    "    setIsExportingPDF(true);\n",
    "    \n",
    "    setTimeout(async () => {\n",
    "      try {\n",
    "        const page1 = document.getElementById('pdf-report-content');\n",
    "        if (!page1) return;\n",
    "        \n",
    "        const canvas1 = await html2canvas(page1, { \n",
    "          scale: 2, \n",
    "          useCORS: true,\n",
    "          windowHeight: page1.scrollHeight\n",
    "        });\n",
    "        const imgData1 = canvas1.toDataURL('image/jpeg', 1.0);\n",
    "        \n",
    "        const pdfWidth = 210; // A4 width in mm\n",
    "        const pdfHeight1 = (canvas1.height * pdfWidth) / canvas1.width;\n",
    "        \n",
    "        // Use dynamic height to avoid cropping\n",
    "        const pdf = new jsPDF('p', 'mm', [pdfWidth, Math.max(297, pdfHeight1)]);\n",
    "        \n",
    "        pdf.addImage(imgData1, 'JPEG', 0, 0, pdfWidth, pdfHeight1);\n",
    "        \n",
    "        pdf.save(`${profile['ROLL NO.'] || profile.ROLL_KEY || 'Student'}_Report.pdf`);\n",
    "      } catch (err) {\n",
    "        console.error('Failed to generate PDF', err);\n",
    "      } finally {\n",
    "        setIsExportingPDF(false);\n",
    "      }\n",
    "    }, 500);\n",
    "  };\n"
]

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if "const exportProfileToPDF = async () => {" in line:
        start_idx = i
    if start_idx != -1 and i > start_idx and "setIsExportingPDF(false);" in line:
        end_idx = i + 3
        break

if start_idx != -1 and end_idx != -1:
    lines = lines[:start_idx] + new_func_lines + lines[end_idx:]
    with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx', 'w') as f:
        f.writelines(lines)
    print("Patched successfully via indices")
else:
    print(f"Failed to find indices. Start: {start_idx}, End: {end_idx}")

