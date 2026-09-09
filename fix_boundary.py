import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Fix opening tag
old_return = "return (\n    <div className=\"fade-in dashboard-page\">"
new_return = "return (\n    <ErrorBoundary>\n    <div className=\"fade-in dashboard-page\">"
if "<ErrorBoundary>\n    <div className=\"fade-in dashboard-page\">" not in content:
    content = content.replace(old_return, new_return)

with open(filepath, 'w') as f:
    f.write(content)
print("Fixed ErrorBoundary opening tag")
