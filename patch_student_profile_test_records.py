import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx'
with open(filepath, 'r') as f:
    content = f.read()

bad = "<TestRecordsTable chartData={chartData} streamCfg={streamCfg} stream={stream} />"
good = "<TestRecordsTable chartData={chartData} streamCfg={streamCfg} stream={stream} profile={profile} />"

if bad in content:
    content = content.replace(bad, good)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched StudentProfileView successfully!")
else:
    print("Could not find TestRecordsTable in StudentProfileView")
