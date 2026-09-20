import re
import os

filepath = "/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx"
with open(filepath, "r") as f:
    content = f.read()

# Replace the condition check
content = content.replace("overallWeakTopicsData.overallWeakTopics", "overallWeakTopicsData.subjectWise")

# Replace subjData fetch
old_subj_fetch = """const subjData = overallWeakTopicsData.subjectWise[subject];
              if (!subjData || (!subjData.strongWeak.length && !subjData.mediumWeak.length)) return null;"""
new_subj_fetch = """const subjKey = subject.toUpperCase();
              const subjData = overallWeakTopicsData.subjectWise[subjKey];
              if (!subjData || (!subjData.weak.length && !subjData.moderate.length)) return null;"""
content = content.replace(old_subj_fetch, new_subj_fetch)

# Replace strongWeak rendering block
old_strongWeak_block = """{subjData.strongWeak.length > 0 && (
                    <div style={{ marginBottom: subjData.mediumWeak.length ? '6px' : '0' }}>
                      <div style={{ fontSize: '9px', fontWeight: 700, color: '#c0392b', textTransform: 'uppercase', marginBottom: '2px' }}>🔴 Weakest</div>
                      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                        {subjData.strongWeak.map(topic => (
                          <span key={topic} style={{ display: 'inline-block', padding: '1px 4px', borderRadius: '3px', fontSize: '8.5px', fontWeight: 700, background: '#fdecea', color: '#c0392b', border: '1px solid #f5a5a5', margin: '1px 3px 1px 0' }}>
                            {topic}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}"""

new_strongWeak_block = """{subjData.weak.length > 0 && (
                    <div style={{ marginBottom: subjData.moderate.length ? '6px' : '0' }}>
                      <div style={{ fontSize: '9px', fontWeight: 700, color: '#c0392b', textTransform: 'uppercase', marginBottom: '2px' }}>🔴 Weakest</div>
                      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                        {subjData.weak.map(topic => (
                          <span key={topic} style={{ display: 'inline-block', padding: '1px 4px', borderRadius: '3px', fontSize: '8.5px', fontWeight: 700, background: '#fdecea', color: '#c0392b', border: '1px solid #f5a5a5', margin: '1px 3px 1px 0' }}>
                            {topic}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}"""
content = content.replace(old_strongWeak_block, new_strongWeak_block)

old_mediumWeak_block = """{subjData.mediumWeak.length > 0 && (
                    <div>
                      <div style={{ fontSize: '9px', fontWeight: 700, color: '#b45309', textTransform: 'uppercase', marginBottom: '2px' }}>🟡 Weak</div>
                      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                        {subjData.mediumWeak.map(topic => (
                          <span key={topic} style={{ display: 'inline-block', padding: '1px 4px', borderRadius: '3px', fontSize: '8.5px', fontWeight: 700, background: '#fff8e1', color: '#b45309', border: '1px solid #fcd5a0', margin: '1px 3px 1px 0' }}>
                            {topic}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}"""
                  
new_mediumWeak_block = """{subjData.moderate.length > 0 && (
                    <div>
                      <div style={{ fontSize: '9px', fontWeight: 700, color: '#b45309', textTransform: 'uppercase', marginBottom: '2px' }}>🟡 Weak</div>
                      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                        {subjData.moderate.map(topic => (
                          <span key={topic} style={{ display: 'inline-block', padding: '1px 4px', borderRadius: '3px', fontSize: '8.5px', fontWeight: 700, background: '#fff8e1', color: '#b45309', border: '1px solid #fcd5a0', margin: '1px 3px 1px 0' }}>
                            {topic}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}"""

content = content.replace(old_mediumWeak_block, new_mediumWeak_block)

with open(filepath, "w") as f:
    f.write(content)
print("Done fixing PDF weak topics.")
