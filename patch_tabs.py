import sys

def remove_student_tab(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if "{ key: 'students'," in line and "'Students'" in line:
            continue
        new_lines.append(line)
        
    with open(filepath, 'w') as f:
        f.writelines(new_lines)
    print(f"Patched {filepath}")

remove_student_tab('/Users/surya/Desktop/CSRL-APP-frontend/src/components/Layout.jsx')
remove_student_tab('/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx')
remove_student_tab('/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx')
