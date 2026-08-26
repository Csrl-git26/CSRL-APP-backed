import sys

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # AdminDashboard / CentreDashboard find
    # data.profiles.find((p) => p.ROLL_KEY === viewingStudentId);
    old_code_1 = "const profile      = data.profiles.find((p) => p.ROLL_KEY === viewingStudentId);"
    new_code_1 = "const profile      = data.profiles.find((p) => String(p.ROLL_KEY) === String(viewingStudentId));"
    
    old_code_2 = "const studentTests = data.tests.find((t) => t.ROLL_KEY === viewingStudentId) || {};"
    new_code_2 = "const studentTests = data.tests.find((t) => String(t.ROLL_KEY) === String(viewingStudentId)) || {};"
    
    if old_code_1 in content:
        content = content.replace(old_code_1, new_code_1)
    if old_code_2 in content:
        content = content.replace(old_code_2, new_code_2)

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed {filepath}")

fix_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx')
fix_file('/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx')
