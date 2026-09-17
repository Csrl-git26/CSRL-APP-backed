from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['csrl']

marks = list(db['studentrawmarks'].find({}).limit(5))
if not marks:
    print("No docs in studentrawmarks")
else:
    for m in marks:
        print(f"centerId: {m.get('centerId')}, testId: {m.get('testId')}")
        
