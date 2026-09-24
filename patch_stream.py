import os

filepath = '/Users/surya/Desktop/CSRL-APP-backed/server.js'
with open(filepath, 'r') as f:
    content = f.read()

old_logic = """const rawStream = p.stream || p.STREAM || p.Stream || 'JEE';"""
new_logic = """let rawStream = p.stream || p.STREAM || p.Stream;
    if (!rawStream) {
      if (p.ROLL_KEY && (p.ROLL_KEY.includes('JRS') || p.ROLL_KEY.includes('TEZ') || p.ROLL_KEY.includes('PUN') || p.ROLL_KEY.includes('GVM') || p.ROLL_KEY.includes('JRT'))) {
        rawStream = 'NEET';
      } else {
        rawStream = 'JEE';
      }
    }"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched filterByStream successfully.")
else:
    print("Could not find old_logic in server.js")
