import csv

with open('uploads/testHistory.csv', 'r') as f:
    reader = csv.DictReader(f)
    tests = list(reader)

validTestKeys = ["MMT01", "MMT02"]

def parseTestColumn(key):
    if '_' in key:
        parts = key.split('_')
        subjRaw = parts[-1]
        tName = '_'.join(parts[:-1])
        aliases = {"PHY": "Physics", "CHEM": "Chemistry", "BOT": "Botany", "ZOO": "Zoology", "BIO": "Biology"}
        subject = aliases.get(subjRaw.upper(), subjRaw)
        return {"testName": tName, "subject": subject}
    return {"testName": key, "subject": "Total"}

def getScoreForDoc(doc, sub, validTestKeys):
    if not doc: return None
    rKeys = list(doc.keys())
    k = None
    for rk in rKeys:
        pcol = parseTestColumn(rk)
        if pcol["testName"] in validTestKeys and pcol["subject"] == sub:
            k = rk
            break
    if not k:
        for rk in rKeys:
            rkUpper = rk.upper()
            subUpper = sub.upper()
            if rkUpper == subUpper or (rkUpper == "PHY" and sub == "Physics") or (rkUpper == "CHEM" and sub == "Chemistry") or (rkUpper == "BOT" and sub == "Botany") or (rkUpper == "ZOO" and sub == "Zoology"):
                k = rk
                break
            if rk.lower().endswith("_" + sub.lower()) or (rkUpper.endswith("_BOT") and sub == "Botany") or (rkUpper.endswith("_ZOO") and sub == "Zoology"):
                k = rk
                break
    if k and doc[k].strip():
        try:
            val = float(doc[k])
            return val if val > 0 else 0
        except ValueError:
            pass
    return None

subjectsSet = set()
allSubjs = ['Physics', 'Chemistry', 'Math', 'Biology', 'Botany', 'Zoology']
for sub in allSubjs:
    for doc in tests:
        if getScoreForDoc(doc, sub, validTestKeys) is not None:
            subjectsSet.add(sub)
            break

print("Subjects:", subjectsSet)

# Check specifically for Khushi (Roll Key = DLK2472018)
khushi = next((t for t in tests if t.get('ROLL_KEY') == 'DLK2472018'), None)
if khushi:
    print("Khushi Botany:", getScoreForDoc(khushi, "Botany", validTestKeys))
    print("Khushi raw Botany keys:", {k:v for k,v in khushi.items() if 'BOT' in k.upper()})

