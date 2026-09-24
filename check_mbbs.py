import pymongo
client = pymongo.MongoClient('mongodb+srv://developer:a5F0g1w0f1Yv74u3@cluster0.o98z0.mongodb.net/csrl_db?retryWrites=true&w=majority&appName=Cluster0')
db = client['csrl_db']
TestScore = db['testscores']
docs = list(TestScore.find({"tests.NCT01": {"$exists": True}}))

mbbs_counts = {}
for doc in docs:
    nct01 = doc.get("tests", {}).get("NCT01", {})
    # Check what the actual keys are
    for k, v in nct01.items():
        if 'mbbs' in k.lower():
            key = f"{k}={v}"
            mbbs_counts[key] = mbbs_counts.get(key, 0) + 1

print("MBBS flags found:")
for k, v in mbbs_counts.items():
    print(f"  {k}: {v} students")
