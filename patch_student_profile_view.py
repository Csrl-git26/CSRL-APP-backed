import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad_def = "export default function StudentProfileView({ profile, studentTests, testColumns }) {"
good_def = "export default function StudentProfileView({ profile, studentTests, testColumns, idSuffix = 'pdf-report-content', isHiddenForBulk = false }) {"

bad_id = "const page1 = document.getElementById('pdf-report-content');"
good_id = "const page1 = document.getElementById(idSuffix);"

bad_report = "<StudentReportCard"
good_report = "<StudentReportCard containerId={idSuffix}"

bad_return = """  return (
    <div style={{ position: 'relative' }}>
      {/* EXPORT BUTTON */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>"""

good_return = """  return (
    <div style={{ position: 'relative' }}>
      {!isHiddenForBulk && (
        <>
          {/* EXPORT BUTTON */}
          <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>"""

bad_hidden_container = """      {/* HIDDEN PRINTABLE CONTAINER */}
      <div style={{ position: 'absolute', left: '0', top: '0', zIndex: -1000, opacity: 0, pointerEvents: 'none' }}>"""

good_hidden_container = """        </>
      )}

      {/* HIDDEN PRINTABLE CONTAINER */}
      <div style={{ position: 'absolute', left: '0', top: '0', zIndex: -1000, opacity: 0, pointerEvents: 'none' }}>"""

if bad_def in content and bad_id in content and bad_return in content and bad_hidden_container in content:
    content = content.replace(bad_def, good_def)
    content = content.replace(bad_id, good_id)
    content = content.replace(bad_report, good_report)
    content = content.replace(bad_return, good_return)
    content = content.replace(bad_hidden_container, good_hidden_container)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched StudentProfileView.jsx successfully.")
else:
    print("Could not find the target strings.")
