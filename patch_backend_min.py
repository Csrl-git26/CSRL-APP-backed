import sys

filepath = '/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js'
with open(filepath, 'r') as f:
    content = f.read()

old_init = "if (!centreAgg[code]) centreAgg[code] = { sum: 0, count: 0, max: -Infinity, studentCount: 0 };"
new_init = "if (!centreAgg[code]) centreAgg[code] = { sum: 0, count: 0, max: -Infinity, min: Infinity, studentCount: 0 };"

old_update = """      if (mark > centreAgg[code].max) centreAgg[code].max = mark;
    });"""
new_update = """      if (mark > centreAgg[code].max) centreAgg[code].max = mark;
      if (mark < centreAgg[code].min) centreAgg[code].min = mark;
    });"""

old_map = """      const top     = s.max === -Infinity ? 0 : s.max;
      const rollSet = new Set("""
new_map = """      const top     = s.max === -Infinity ? 0 : s.max;
      const bottom  = s.min === Infinity ? 0 : s.min;
      const rollSet = new Set("""

old_return = "return { code, avg, top, tested: s.count, studentCount: s.studentCount, weakSubject };"
new_return = "return { code, avg, top, bottom, tested: s.count, studentCount: s.studentCount, weakSubject };"

content = content.replace(old_init, new_init)
content = content.replace(old_update, new_update)
content = content.replace(old_map, new_map)
content = content.replace(old_return, new_return)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched analyticsService.js for lowest score")
