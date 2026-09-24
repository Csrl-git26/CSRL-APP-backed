import pymongo

uri = "mongodb+srv://developer:a5F0g1w0f1Yv74u3@cluster0.o98z0.mongodb.net/csrl_db?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(uri)
db = client.get_default_database()
TestScore = db['testscores']

count_Mbbs = TestScore.count_documents({"tests.NCT01.Mbbs": {"$exists": True}})
count_MBBS = TestScore.count_documents({"tests.NCT01.MBBS": {"$exists": True}})
count_mbbs = TestScore.count_documents({"tests.NCT01.mbbs": {"$exists": True}})
count_total = TestScore.count_documents({"tests.NCT01": {"$exists": True}})

# wait, there's another format the flag might have been saved as:
count_NCT01_MBBS = TestScore.count_documents({"NCT01_MBBS": {"$exists": True}})
count_NCT01_Mbbs = TestScore.count_documents({"NCT01_Mbbs": {"$exists": True}})

print(f"tests.NCT01.Mbbs: {count_Mbbs}")
print(f"tests.NCT01.MBBS: {count_MBBS}")
print(f"tests.NCT01.mbbs: {count_mbbs}")
print(f"NCT01_MBBS: {count_NCT01_MBBS}")
print(f"NCT01_Mbbs: {count_NCT01_Mbbs}")
print(f"Total NCT01 test records: {count_total}")
