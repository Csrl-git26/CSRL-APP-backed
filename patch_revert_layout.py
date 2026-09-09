import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/InsightsDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace the start of the layout
old_start = """      {/* ── Main Dashboard Layout ── */}
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1.8fr)', gap: 20 }}>
        
        {/* Left Column: Top 5 Students */}
        <div style={{ background:'#fff', borderRadius:14, padding:'18px 20px',
          boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e8f0fc', alignSelf: 'start' }}>"""

new_start = """      {/* ── Top 5 Students ── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 20, marginBottom: 20 }}>
        <div style={{ background:'#fff', borderRadius:14, padding:'18px 20px',
          boxShadow:'0 2px 8px rgba(0,0,0,0.07)', border:'1px solid #e8f0fc' }}>"""

if old_start in content:
    content = content.replace(old_start, new_start)
else:
    print("Error: old_start not found")

# Replace the middle part where Right Column starts
old_middle = """          }
        </div>

      {/* Right Column: Top 10 Centres Cards & Pie Chart ── */}"""

new_middle = """          }
        </div>
      </div>

      {/* ── Top/Bottom Centres & Pie Chart ── */}"""

if old_middle in content:
    content = content.replace(old_middle, new_middle)
else:
    print("Error: old_middle not found")

# Remove the closing div at the end
old_end = """        );
      })()}
      
      </div> {/* End Main Dashboard Layout */}

    </div>
  );
}"""

new_end = """        );
      })()}

    </div>
  );
}"""

if old_end in content:
    content = content.replace(old_end, new_end)
else:
    print("Error: old_end not found")

with open(filepath, 'w') as f:
    f.write(content)

print("Layout reverted to vertical successfully")
