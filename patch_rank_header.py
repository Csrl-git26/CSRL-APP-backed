import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # The string to find is: {t.replace('FMT','')} Rk
    old_str = "{t.replace('FMT','')} Rk"
    new_str = "{t} Rank"
    
    if old_str in content:
        content = content.replace(old_str, new_str)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Patched {filepath}")
    else:
        print(f"Could not find old_str in {filepath}")

patch_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx')
patch_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx')
