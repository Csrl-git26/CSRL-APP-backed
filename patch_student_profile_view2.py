import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Update export function signature
bad_sig = "export default function StudentProfileView({ profile, studentTests, testColumns }) {"
good_sig = "export default function StudentProfileView({ profile, studentTests, testColumns, isHiddenForBulk = false }) {"

# 2. Update getElementById inside exportProfileToPDF
bad_get = "const page1 = document.getElementById('pdf-report-content');"
good_get = "const page1 = document.getElementById(`pdf-report-content-${profile.ROLL_KEY}`);"

# 3. Update return statement to hide UI if isHiddenForBulk
bad_ret = """  return (
    <div style={{ position: 'relative' }}>
      {/* EXPORT BUTTON */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>"""

good_ret = """  return (
    <div style={{ position: 'relative' }}>
      {!isHiddenForBulk && (
      <>
      {/* EXPORT BUTTON */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>"""

# 4. Update the hidden container
bad_hidden = """      {/* HIDDEN PRINTABLE CONTAINER */}
      <div style={{ position: 'absolute', left: '0', top: '0', zIndex: -1000, opacity: 0, pointerEvents: 'none' }}>
        <StudentReportCard
          profile={profile}"""

good_hidden = """      </>
      )}
      {/* HIDDEN PRINTABLE CONTAINER */}
      <div style={{ position: 'absolute', left: '0', top: '0', zIndex: -1000, opacity: 0, pointerEvents: 'none' }}>
        <StudentReportCard
          containerId={`pdf-report-content-${profile.ROLL_KEY}`}
          profile={profile}"""


content = content.replace(bad_sig, good_sig)
content = content.replace(bad_get, good_get)
content = content.replace(bad_ret, good_ret)
content = content.replace(bad_hidden, good_hidden)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched StudentProfileView successfully.")
