import sys

def patch_file(filepath, old_str, new_str):
    with open(filepath, 'r') as f:
        content = f.read()
    if old_str in content:
        content = content.replace(old_str, new_str)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Patched {filepath}")
    else:
        print(f"Not found in {filepath}")

patch_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/Layout.jsx', 'CSRL Admin', 'CSRL Management')
patch_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx', 'CSRL Admin', 'CSRL Management')
