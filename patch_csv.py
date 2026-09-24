import os

filepath = '/Users/surya/Desktop/CSRL-APP-backed/services/csvParserService.js'
with open(filepath, 'r') as f:
    content = f.read()

# Fix location alias
old_loc = "if (low === 'location' || low === 'centre' || low === 'center' || low === 'centrecode' || low === 'centercode') return '__location__';"
new_loc = "if (low === 'location' || low === 'centre' || low === 'center' || low === 'centrecode' || low === 'centercode' || low === 'centre code' || low === 'center code') return '__location__';"

content = content.replace(old_loc, new_loc)

# Fix roll alias
old_roll = "if (low === 'roll no.' || low === 'roll no' || low === 'roll_no' || low === 'rollno' || low === 'roll_key' || low === 'roll') return '__roll__';"
new_roll = "if (low === 'roll no.' || low === 'roll no' || low === 'roll_no' || low === 'rollno' || low === 'roll_key' || low === 'roll' || low === 'roll number') return '__roll__';"

content = content.replace(old_roll, new_roll)

with open(filepath, 'w') as f:
    f.write(content)

print("Patched csvParserService.js aliases successfully.")
