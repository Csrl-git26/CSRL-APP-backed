import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad_ret = """  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {/* Banner */}"""

good_ret = """  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {!isHiddenForBulk && (
      <>
      {/* Banner */}"""

bad_hidden = """      {/* HIDDEN PRINTABLE CONTAINER */}
      <div style={{ position: 'absolute', left: '0', top: '0', zIndex: -1000, opacity: 0, pointerEvents: 'none' }}>
        <StudentReportCard
          containerId={`pdf-report-content-${profile.ROLL_KEY}`}"""

good_hidden = """      </>
      )}
      {/* HIDDEN PRINTABLE CONTAINER */}
      <div style={{ position: 'absolute', left: '0', top: '0', zIndex: -1000, opacity: 0, pointerEvents: 'none' }}>
        <StudentReportCard
          containerId={`pdf-report-content-${profile.ROLL_KEY}`}"""

if bad_ret in content and bad_hidden in content:
    content = content.replace(bad_ret, good_ret)
    content = content.replace(bad_hidden, good_hidden)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Fixed StudentProfileView.jsx successfully.")
else:
    print("Could not find the target strings in StudentProfileView.jsx.")

