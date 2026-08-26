import sys

filepath = '/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js'
with open(filepath, 'r') as f:
    content = f.read()

old_smin = "subjectMins[subj] = 20; // 20 marks per subject for all categories"
new_smin = "subjectMins[subj] = 30; // 30 marks per subject for all categories"

if old_smin in content:
    content = content.replace(old_smin, new_smin)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched analyticsService.js successfully!")
else:
    print("Could not find old_smin in analyticsService.js")
