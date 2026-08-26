import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestInsightsPanel.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_title = '<div className="section-title">Below subject cutoff — count by centre</div>'
new_title = '<div className="section-title">student no. subjectwise marks &lt;=30 - count by centre</div>'

if old_title in content:
    content = content.replace(old_title, new_title)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched title successfully!")
else:
    print("Could not find old_title in TestInsightsPanel.jsx")
    
# Remove subtitle
import re
# Look for <p style={{ fontSize: 12 ... }}> ... </p> immediately following the title
subtitle_pattern = r'<p style={{ fontSize: 12, color: \'var\(--gray-600\)\', marginBottom: 12 }}>\s*Students with a subject mark below their stream&apos;s cutoff \(\{Math\.round\(\(cut\?\.subjectQualifyRatio \?\? 0\.35\) \* 100\)\}% of that subject&apos;s max — JEE vs NEET differ\)\.\s*</p>'
if re.search(subtitle_pattern, content):
    content = re.sub(subtitle_pattern, '', content)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched subtitle successfully!")
else:
    print("Could not find subtitle in TestInsightsPanel.jsx")
