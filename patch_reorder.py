import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """      <div style={{ marginTop: '24px' }}>
        <StudentOverallWeakTopics studentId={profile.ROLL_KEY} />
      </div>

      <PerformanceChart chartData={chartData} streamCfg={streamCfg} />
      <TestRecordsTable chartData={chartData} streamCfg={streamCfg} stream={stream} profile={profile} />"""

new_block = """      <PerformanceChart chartData={chartData} streamCfg={streamCfg} />
      <TestRecordsTable chartData={chartData} streamCfg={streamCfg} stream={stream} profile={profile} />

      <div style={{ marginTop: '24px' }}>
        <StudentOverallWeakTopics studentId={profile.ROLL_KEY} />
      </div>"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched StudentProfileView.jsx to reorder components")
else:
    print("WARNING: Could not find block to replace in StudentProfileView.jsx")
