import sys

filepath = '/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js'
with open(filepath, 'r') as f:
    content = f.read()

old_absent = """        gender:   p.GENDER || '',
        stream:   p.stream     || (testDoc ? testDoc.stream : 'JEE'),
        photo:    p['STUDENT PHOTO URL'] || null,
        rank:     '-'
      });"""

new_absent = """        gender:   p.GENDER || '',
        stream:   p.stream     || (testDoc ? testDoc.stream : 'JEE'),
        photo:    p['STUDENT PHOTO URL'] || null,
        rank:     '-',
        rawScores: testDoc || {}
      });"""

old_scored = """        gender:   p.GENDER || '',
        stream:   p.stream     || (testDoc ? testDoc.stream : 'JEE'),
        photo:    p['STUDENT PHOTO URL'] || null,
      });"""

new_scored = """        gender:   p.GENDER || '',
        stream:   p.stream     || (testDoc ? testDoc.stream : 'JEE'),
        photo:    p['STUDENT PHOTO URL'] || null,
        rawScores: testDoc || {}
      });"""

content = content.replace(old_absent, new_absent)
content = content.replace(old_scored, new_scored)

with open(filepath, 'w') as f:
    f.write(content)

print("Patched rankStudentsByTest")
