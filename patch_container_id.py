import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad1 = """  examResult,
  examLabel,
}) {"""

good1 = """  examResult,
  examLabel,
  containerId = "pdf-report-content",
}) {"""

bad2 = """  return (
    <>
    <div id="pdf-report-content" style={{
      width: '800px',"""

good2 = """  return (
    <>
    <div id={containerId} style={{
      width: '800px',"""

if bad1 in content and bad2 in content:
    content = content.replace(bad1, good1).replace(bad2, good2)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched containerId successfully.")
else:
    print("Could not find the target strings.")
