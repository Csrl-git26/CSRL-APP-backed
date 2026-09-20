import os
import re

filepath = "/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx"
with open(filepath, "r") as f:
    content = f.read()

# Replace the header
content = content.replace("Detailed Weak Topics Analysis", "Overall Topic Performance")

# Replace the condition for showing subject
old_condition = "if (!subjData || (!subjData.weak.length && !subjData.moderate.length)) return null;"
new_condition = "if (!subjData || (!subjData.weak.length && !subjData.moderate.length && !subjData.strong.length)) return null;"
content = content.replace(old_condition, new_condition)

# We need to replace the entire rendering block for topics within the subject card.
# The easiest way is to use regex or find the exact string.

old_topics_block = """{subjData.weak.length > 0 && (
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
                  )}

                  {subjData.moderate.length > 0 && (
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

new_topics_block = """{subjData.strong.length > 0 && (
                    <div style={{ marginBottom: (subjData.moderate.length || subjData.weak.length) ? '6px' : '0' }}>
                      <div style={{ fontSize: '9px', fontWeight: 700, color: '#166534', textTransform: 'uppercase', marginBottom: '2px' }}>🟢 Strong</div>
                      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                        {subjData.strong.map(topic => (
                          <span key={topic} style={{ display: 'inline-block', padding: '1px 4px', borderRadius: '3px', fontSize: '8.5px', fontWeight: 700, background: '#f0fdf4', color: '#166534', border: '1px solid #bbf7d0', margin: '1px 3px 1px 0' }}>
                            {topic}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {subjData.moderate.length > 0 && (
                    <div style={{ marginBottom: subjData.weak.length ? '6px' : '0' }}>
                      <div style={{ fontSize: '9px', fontWeight: 700, color: '#b45309', textTransform: 'uppercase', marginBottom: '2px' }}>🟡 Moderate</div>
                      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                        {subjData.moderate.map(topic => (
                          <span key={topic} style={{ display: 'inline-block', padding: '1px 4px', borderRadius: '3px', fontSize: '8.5px', fontWeight: 700, background: '#fff8e1', color: '#b45309', border: '1px solid #fcd5a0', margin: '1px 3px 1px 0' }}>
                            {topic}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {subjData.weak.length > 0 && (
                    <div>
                      <div style={{ fontSize: '9px', fontWeight: 700, color: '#c0392b', textTransform: 'uppercase', marginBottom: '2px' }}>🔴 Weak</div>
                      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                        {subjData.weak.map(topic => (
                          <span key={topic} style={{ display: 'inline-block', padding: '1px 4px', borderRadius: '3px', fontSize: '8.5px', fontWeight: 700, background: '#fdecea', color: '#c0392b', border: '1px solid #f5a5a5', margin: '1px 3px 1px 0' }}>
                            {topic}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}"""

content = content.replace(old_topics_block, new_topics_block)

with open(filepath, "w") as f:
    f.write(content)

print("Updated PDF rendering logic.")
