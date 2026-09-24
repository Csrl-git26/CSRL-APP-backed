import os
filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_str = '"No. of student subjectwise marks <=20"'
new_str = 'streamFilter === "NEET" ? "No. of student subjectwise marks <=100" : "No. of student subjectwise marks <=20"'
if old_str in content:
    content = content.replace(old_str, new_str)
    
old_str2 = '`No. of student marks in ${selectedSubject} <=20`'
new_str2 = '`No. of student marks in ${selectedSubject} <=${streamFilter === "NEET" ? 100 : 20}`'
if old_str2 in content:
    content = content.replace(old_str2, new_str2)

with open(filepath, 'w') as f:
    f.write(content)
print('CentreLeaderboard patched!')
