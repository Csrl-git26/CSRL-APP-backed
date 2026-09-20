import re

def parse_sequence(name):
    match = re.match(r"^([A-Za-z\-]+)(\d+)(.*)$", name)
    if not match:
        return None
    prefix = re.sub(r'[^A-Z]', '', match.group(1).upper())
    num = int(match.group(2))
    return {"prefix": prefix, "num": num}

def get_logical_index(seq):
    if not seq:
        return -1
    prefix = seq["prefix"]
    num = seq["num"]
    if prefix in ['MT', 'PT']:
        return num * 10
    if prefix in ['CMT', 'JCT']:
        return num * 20 + 5
    if prefix == 'FMT':
        return 1000 + num * 10
    return -1

def sort_key(test):
    name = test["name"]
    seq = parse_sequence(name)
    idx = get_logical_index(seq)
    
    # We can return a tuple for sorting: (idx if found else float('inf'), name)
    if idx != -1:
        return (0, idx, name)
    return (1, 0, name)

tests = [
  { "name": 'MT02' },
  { "name": 'CMT01' },
  { "name": 'MT01' },
  { "name": 'MT03' },
  { "name": 'CMT02' },
  { "name": 'FMT01' },
  { "name": 'MT04' }
]

tests.sort(key=sort_key)
print([t["name"] for t in tests])
