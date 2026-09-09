import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

target1 = "export default function InsightsDashboard({ data, overview, topRanked, bottomRanked, centreBoard, selectedTestKey, onViewStudent }) {"
repl1 = "export default function InsightsDashboard({ data, overview, topRanked, bottomRanked, centreBoard, selectedTestKey, onViewStudent, onViewCentre }) {"
content = content.replace(target1, repl1)

target2 = """              return (
                <div key={c.code} style={{ padding:'12px 10px', borderRadius:10, textAlign:'center',
                  background: isAlert ? '#fef2f2' : '#f8fafc',
                  border: isAlert ? '1px solid #fecaca' : '1px solid #e2e8f0' }}>"""
repl2 = """              return (
                <div key={c.code} style={{ padding:'12px 10px', borderRadius:10, textAlign:'center',
                  background: isAlert ? '#fef2f2' : '#f8fafc',
                  border: isAlert ? '1px solid #fecaca' : '1px solid #e2e8f0',
                  cursor: onViewCentre ? 'pointer' : 'default' }}
                  onClick={() => onViewCentre && onViewCentre(c.code)}>"""
content = content.replace(target2, repl2)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched InsightsDashboard.jsx")
