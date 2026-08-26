import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad = "overallWeakTopicsData={overallWeakTopicsData}"
good = "overallWeakTopicsData={actualWeakTopics}"

if bad in content:
    content = content.replace(bad, good)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched overallWeakTopicsData prop successfully")
else:
    print("Could not find overallWeakTopicsData prop")
