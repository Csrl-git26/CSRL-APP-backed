import os

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_button = """<button type="button" className="btn btn-outline btn-sm" onClick={downloadMarksSampleFormat}><Download size={13} /> Download sample format</button>
<button type="button" className="btn btn-outline btn-sm" onClick={exportMarksXlsx}><Download size={13} /> Export selected test</button>"""
new_button = """<button type="button" className="btn btn-outline btn-sm" onClick={downloadMarksSampleFormat}><Download size={13} /> JEE sample format</button>
<button type="button" className="btn btn-outline btn-sm" onClick={downloadNeetMarksSampleFormat}><Download size={13} /> NEET sample format</button>
<button type="button" className="btn btn-outline btn-sm" onClick={exportMarksXlsx}><Download size={13} /> Export selected test</button>"""

content = content.replace(old_button, new_button)

old_function = """  const downloadMarksSampleFormat = () => {
    const rows = [
      ['Roll Number', 'name', 'stream', 'centre', 'Physics', 'Chemistry', 'Mathematics', 'Marks'],
      ['GAIL-JEE-001', 'John Doe', 'JEE', 'GAIL', 40, 50, 30, 120],
      ['GAIL-JEE-002', 'Jane Smith', 'JEE', 'GAIL', 50, 60, 40, 150]
    ];
    const ws = XLSX.utils.aoa_to_sheet(rows);
    ws['!cols'] = [{ wch: 15 }, { wch: 20 }, { wch: 10 }, { wch: 10 }, { wch: 10 }, { wch: 10 }, { wch: 12 }, { wch: 10 }];
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Marks Template');
    XLSX.writeFile(wb, 'CSRL_Marks_Template.xlsx');
  };"""

new_function = """  const downloadMarksSampleFormat = () => {
    const rows = [
      ['Roll Number', 'name', 'stream', 'centre', 'Physics', 'Chemistry', 'Mathematics', 'Marks'],
      ['GAIL-JEE-001', 'John Doe', 'JEE', 'GAIL', 40, 50, 30, 120],
      ['GAIL-JEE-002', 'Jane Smith', 'JEE', 'GAIL', 50, 60, 40, 150]
    ];
    const ws = XLSX.utils.aoa_to_sheet(rows);
    ws['!cols'] = [{ wch: 15 }, { wch: 20 }, { wch: 10 }, { wch: 10 }, { wch: 10 }, { wch: 10 }, { wch: 12 }, { wch: 10 }];
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Marks Template');
    XLSX.writeFile(wb, 'CSRL_Marks_Template.xlsx');
  };

  const downloadNeetMarksSampleFormat = () => {
    const rows = [
      ['Roll Number', 'name', 'stream', 'centre', 'Physics', 'Chemistry', 'Botany', 'Zoology', 'Total'],
      ['GAIL-NEET-001', 'John Doe', 'NEET', 'GAIL', 140, 150, 130, 160, 580],
      ['GAIL-NEET-002', 'Jane Smith', 'NEET', 'GAIL', 150, 160, 140, 170, 620]
    ];
    const ws = XLSX.utils.aoa_to_sheet(rows);
    ws['!cols'] = [{ wch: 15 }, { wch: 20 }, { wch: 10 }, { wch: 10 }, { wch: 10 }, { wch: 10 }, { wch: 10 }, { wch: 10 }, { wch: 10 }];
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'NEET Marks Template');
    XLSX.writeFile(wb, 'CSRL_NEET_Marks_Template.xlsx');
  };"""

content = content.replace(old_function, new_function)

with open(filepath, 'w') as f:
    f.write(content)

print("Frontend patched.")
