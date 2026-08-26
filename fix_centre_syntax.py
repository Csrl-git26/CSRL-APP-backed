import sys

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove the bad backslashes
    content = content.replace("\\'FMT\\'", "'FMT'")
    content = content.replace("\\'ALL_FMT\\'", "'ALL_FMT'")
    content = content.replace("\\'var(--gray-400)\\'", "'var(--gray-400)'")
    content = content.replace("\\'center\\'", "'center'")
    content = content.replace("\\'-\\'", "'-'")

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed {filepath}")

patch_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx')
