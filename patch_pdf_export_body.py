import sys

with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx', 'r') as f:
    content = f.read()

old_func = """  const exportProfileToPDF = async () => {
    if (!profile) return;
    setIsExportingPDF(true);
    
    setTimeout(async () => {
      try {
        const page1 = document.getElementById('pdf-report-content');
        if (!page1) return;
        
        const canvas1 = await html2canvas(page1, { 
          scale: 2, 
          useCORS: true,
          windowHeight: page1.scrollHeight,
          height: page1.scrollHeight,
          windowWidth: 800,
          width: 800
        });
        const imgData1 = canvas1.toDataURL('image/jpeg', 1.0);
        
        const pdfWidth = 210; // A4 width in mm
        const pdfHeight1 = (canvas1.height * pdfWidth) / canvas1.width;
        
        // Use dynamic height to avoid cropping
        const pdf = new jsPDF('p', 'mm', [pdfWidth, Math.max(297, pdfHeight1)]);
        
        pdf.addImage(imgData1, 'JPEG', 0, 0, pdfWidth, pdfHeight1);
        
        pdf.save(`${profile['ROLL NO.'] || profile.ROLL_KEY || 'Student'}_Report.pdf`);
      } catch (err) {
        console.error('Failed to generate PDF', err);
      } finally {
        setIsExportingPDF(false);
      }
    }, 500);
  };"""

new_func = """  const exportProfileToPDF = async () => {
    if (!profile) return;
    setIsExportingPDF(true);
    
    setTimeout(async () => {
      try {
        const page1 = document.getElementById('pdf-report-content');
        if (!page1) return;
        
        // Temporarily move to body to avoid overflow clipping from parent modals/tabs
        const originalParent = page1.parentNode;
        const tempContainer = document.createElement('div');
        tempContainer.style.position = 'absolute';
        tempContainer.style.top = '0';
        tempContainer.style.left = '0';
        tempContainer.style.width = '800px';
        tempContainer.style.zIndex = '-9999';
        tempContainer.style.opacity = '0';
        document.body.appendChild(tempContainer);
        tempContainer.appendChild(page1);

        // Wait a frame for layout recalculation
        await new Promise(r => setTimeout(r, 100));

        const canvas1 = await html2canvas(page1, { 
          scale: 2, 
          useCORS: true,
          windowHeight: page1.scrollHeight,
          height: page1.scrollHeight,
          windowWidth: 800,
          width: 800
        });
        
        // Restore to original parent
        originalParent.appendChild(page1);
        document.body.removeChild(tempContainer);

        const imgData1 = canvas1.toDataURL('image/jpeg', 1.0);
        
        const pdfWidth = 210; // A4 width in mm
        const pdfHeight1 = (canvas1.height * pdfWidth) / canvas1.width;
        
        // Use dynamic height to avoid cropping
        const pdf = new jsPDF('p', 'mm', [pdfWidth, Math.max(297, pdfHeight1)]);
        
        pdf.addImage(imgData1, 'JPEG', 0, 0, pdfWidth, pdfHeight1);
        
        pdf.save(`${profile['ROLL NO.'] || profile.ROLL_KEY || 'Student'}_Report.pdf`);
      } catch (err) {
        console.error('Failed to generate PDF', err);
      } finally {
        setIsExportingPDF(false);
      }
    }, 500);
  };"""

if old_func in content:
    content = content.replace(old_func, new_func)
    with open('/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx', 'w') as f:
        f.write(content)
    print("Patched successfully via string replace")
else:
    print("Could not find old_func string in file.")
