import pymongo

client = pymongo.MongoClient('mongodb+srv://surya:qIqg2X2a537fK63s@csrl.6dhyi.mongodb.net/csrl_db?retryWrites=true&w=majority')
db = client['csrl_db']
Profile = db['profiles']
TestScore = db['testscores']

profiles = list(Profile.find({"centerCode": "ONGC-AGR"}))
roll_keys = [p.get("ROLL_KEY") or p.get("rollKey") for p in profiles]
tests = list(TestScore.find({"ROLL_KEY": {"$in": roll_keys}}))

accTotals = {}
accCounts = {}

for t in tests:
    t_tests = t.get("tests", {})
    # Check FMT08
    fmt08 = t_tests.get("FMT08", {})
    for subject, val in fmt08.items():
        if "_Accuracy" in subject:
            subName = subject.replace("_Accuracy", "")
            try:
                mark = float(val)
                accTotals[subName] = accTotals.get(subName, 0) + mark
                accCounts[subName] = accCounts.get(subName, 0) + 1
            except (ValueError, TypeError):
                pass
                
    # Check rogue metrics that didn't get grouped under FMT08
    for key, testData in t_tests.items():
        if "_Accuracy" in key:
            subName = key.replace("_Accuracy", "")
            try:
                mark = float(testData.get("total", testData.get("Total", 0)))
                accTotals[subName] = accTotals.get(subName, 0) + mark
                accCounts[subName] = accCounts.get(subName, 0) + 1
            except (ValueError, TypeError):
                pass

print("ACCURACY AVERAGES FOR ONGC-AGR (FMT08):")
for sub in accTotals.keys():
    avg = accTotals[sub] / accCounts[sub]
    print(f"{sub}: {avg:.1f}% (Count: {accCounts[sub]})")

