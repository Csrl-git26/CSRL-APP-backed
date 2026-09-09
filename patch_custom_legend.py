import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Update legendPayload to include rank
old_payload = """              const legendPayload = top5Qual.map((c, i) => ({
                value: c.code,
                type: 'square',
                color: colors[i % colors.length]
              }));"""

new_payload = """              const legendPayload = top5Qual.map((c, i) => {
                const rank = sortedByQual.findIndex(x => x.code === c.code) + 1;
                return {
                  value: `${rank}. ${c.code}`,
                  type: 'square',
                  color: colors[i % colors.length]
                };
              });"""

content = content.replace(old_payload, new_payload)

# Replace <Legend /> with custom content
old_legend = """<Legend iconSize={8} layout="vertical" verticalAlign="middle" wrapperStyle={{ right: 0, fontSize: 10 }} payload={legendPayload} />"""

new_legend = """<Legend 
                      layout="vertical" 
                      verticalAlign="middle" 
                      wrapperStyle={{ right: 0 }} 
                      content={(props) => (
                        <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                          {legendPayload.map((entry, index) => (
                            <li key={`item-${index}`} style={{ display: 'flex', alignItems: 'center', marginBottom: 4, fontSize: 10, color: entry.color, fontWeight: 700 }}>
                              <span style={{ width: 8, height: 8, backgroundColor: entry.color, marginRight: 6, display: 'inline-block' }}></span>
                              {entry.value}
                            </li>
                          ))}
                        </ul>
                      )}
                    />"""

content = content.replace(old_legend, new_legend)

with open(filepath, 'w') as f:
    f.write(content)

print("Added custom Legend renderer to guarantee descending order and include ranks.")
