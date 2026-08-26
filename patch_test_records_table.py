import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestRecordsTable.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad_sig = "export default function TestRecordsTable({ chartData, streamCfg, stream, isCentre }) {"
good_sig = "export default function TestRecordsTable({ chartData, streamCfg, stream, isCentre, profile }) {"
content = content.replace(bad_sig, good_sig)

old_logic = """                if (stream === 'JEE') {
                  if (tot >= 120 && p >= 35 && c >= 35 && m >= 35) {
                    isQualified = true;
                  }
                } else if (stream === 'NEET') {
                  if (tot >= 550 && b >= 126 && p >= 63 && c >= 63) {
                    isQualified = true;
                  }
                }"""

new_logic = """                if (stream === 'JEE') {
                  const cat = (profile?.CATEGORY || '').toUpperCase().trim();
                  let overallMin = 110;
                  if (cat.includes('PWD')) overallMin = 30;
                  else if (cat.includes('ST')) overallMin = 60;
                  else if (cat.includes('SC')) overallMin = 65;
                  else if (cat.includes('OBC')) overallMin = 85;
                  else if (cat.includes('EWS')) overallMin = 90;
                  
                  if (tot >= overallMin && p >= 20 && c >= 20 && m >= 20) {
                    isQualified = true;
                  }
                } else if (stream === 'NEET') {
                  if (tot >= 550 && b >= 126 && p >= 63 && c >= 63) {
                    isQualified = true;
                  }
                }"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched TestRecordsTable.jsx successfully!")
else:
    print("Could not find the old logic block in TestRecordsTable.jsx")
