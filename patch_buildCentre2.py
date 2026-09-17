import re

with open('/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js', 'r') as f:
    content = f.read()

# We need to find the array and replace it
old_array = "['Physics', 'Chemistry', 'Math', 'Biology'].forEach(sub => {"
new_array = "['Physics', 'Chemistry', 'Math', 'Biology', 'Botany', 'Zoology'].forEach(sub => {"

if old_array in content:
    content = content.replace(old_array, new_array)
    with open('/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js', 'w') as f:
        f.write(content)
    print("Patched buildCentreChartData successfully")
else:
    print("Could not find array in buildCentreChartData")
