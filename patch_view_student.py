import sys

files = [
    '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx',
    '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
]

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()
    
    old_admin = "testKey={selectedTestKey}"
    new_admin = "testKey={selectedTestKey}\n          onViewStudent={setViewingStudentId}"
    
    if old_admin in content:
        content = content.replace(old_admin, new_admin)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Patched {filepath}")
    else:
        print(f"Could not find testKey in {filepath}")

