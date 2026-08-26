import sys

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx', 'r') as f:
    content = f.read()

# Replace exportProfileToPDF
old_export = """  const exportProfileToPDF = async () => {
    if (!profile) return;
    setIsExportingPDF(true);
    
    setTimeout(async () => {
      try {
        const page1 = document.getElementById('pdf-report-content');
        const page2 = document.getElementById('pdf-report-page2');
        if (!page1) return;
        
        const canvas1 = await html2canvas(page1, { scale: 2, useCORS: true });
        const imgData1 = canvas1.toDataURL('image/jpeg', 1.0);
        
        const pdf = new jsPDF('p', 'mm', 'a4');
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight1 = (canvas1.height * pdfWidth) / canvas1.width;
        
        pdf.addImage(imgData1, 'JPEG', 0, 0, pdfWidth, pdfHeight1);
        
        if (page2) {
          const canvas2 = await html2canvas(page2, { scale: 2, useCORS: true });
          const imgData2 = canvas2.toDataURL('image/jpeg', 1.0);
          const pdfHeight2 = (canvas2.height * pdfWidth) / canvas2.width;
          pdf.addPage();
          pdf.addImage(imgData2, 'JPEG', 0, 0, pdfWidth, pdfHeight2);
        }
        
        pdf.save(`${profile['ROLL NO.'] || profile.ROLL_KEY || 'Student'}_Report.pdf`);
      } catch (err) {
        console.error('Failed to generate PDF', err);
      } finally {
        setIsExportingPDF(false);
      }
    }, 500);
  };"""

new_export = """  const exportProfileToPDF = async () => {
    if (!profile) return;
    setIsExportingPDF(true);
    
    setTimeout(async () => {
      try {
        const page1 = document.getElementById('pdf-report-content');
        if (!page1) return;
        
        const canvas1 = await html2canvas(page1, { scale: 2, useCORS: true });
        const imgData1 = canvas1.toDataURL('image/jpeg', 1.0);
        
        // standard a4 width is 210mm
        const pdfWidth = 210;
        const pdfHeight1 = (canvas1.height * pdfWidth) / canvas1.width;
        
        const pdf = new jsPDF('p', 'mm', [pdfWidth, pdfHeight1]);
        
        pdf.addImage(imgData1, 'JPEG', 0, 0, pdfWidth, pdfHeight1);
        
        pdf.save(`${profile['ROLL NO.'] || profile.ROLL_KEY || 'Student'}_Report.pdf`);
      } catch (err) {
        console.error('Failed to generate PDF', err);
      } finally {
        setIsExportingPDF(false);
      }
    }, 500);
  };"""

if old_export in content:
    content = content.replace(old_export, new_export)
    with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx', 'w') as f:
        f.write(content)
    print("Patched StudentProfileView successfully")
else:
    print("Could not find old_export in StudentProfileView")

