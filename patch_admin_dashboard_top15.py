import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Replace limit: 30
content = content.replace("limit: 30, order: 'desc'", "limit: 15, order: 'desc'")
content = content.replace("limit: 30, order: 'asc'", "limit: 15, order: 'asc'")

# Replace Top 30
content = content.replace("Top 30 — {selectedTestKey}", "Top 15 — {selectedTestKey}")

# Replace Bottom 30
content = content.replace("Bottom 30 — {selectedTestKey}", "Bottom 15 — {selectedTestKey}")

with open(filepath, 'w') as f:
    f.write(content)

print("Replaced 30 with 15 successfully!")
