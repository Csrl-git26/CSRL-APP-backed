import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """    const studentTests = data.tests.find((t) => {
      const rk = t.ROLL_KEY != null ? String(t.ROLL_KEY).trim().toLowerCase() : '';
      return rk === target || t.ROLL_KEY === viewingStudentId;
    }) || {};"""

new_code = """    const studentTests = data.tests.find((t) => {
      const rk = t.ROLL_KEY != null ? String(t.ROLL_KEY).trim().toLowerCase() : '';
      return rk === target || t.ROLL_KEY === viewingStudentId;
    }) || {};
    
    // Ultimate fallback if profile is still undefined
    const finalProfile = profile || {
      ROLL_KEY: viewingStudentId,
      "STUDENT'S NAME": "Student " + viewingStudentId,
      roll: viewingStudentId
    };"""

content = content.replace(old_code, new_code)
content = content.replace("<StudentProfileView profile={profile}", "<StudentProfileView profile={finalProfile}")

with open(filepath, 'w') as f:
    f.write(content)
print("Patched admin fallback")
