import pymongo
from pprint import pprint

client = pymongo.MongoClient('mongodb+srv://admin:YtL8ZtOaJ2sA8E6@csrl-app.2e1i8.mongodb.net/csrl_db?retryWrites=true&w=majority')
db = client['csrl_db']

rohit = db.studentweaktopics.find_one({"studentId": "2701073"})
print("Rohit WeakTopics:")
pprint(rohit)

rohit_overall = db.studentoverallweaktopics.find_one({"studentId": "2701073"})
print("\nRohit Overall:")
pprint(rohit_overall)

# Check StudentRawMarks for Rohit
marks = list(db.studentrawmarks.find({"studentId": "2701073"}))
print(f"\nRohit Raw Marks entries: {len(marks)}")

# See how many students were uploaded for MT02
mt02_marks = db.studentrawmarks.count_documents({"testId": "MT02"})
print(f"\nMT02 Raw Marks count: {mt02_marks}")

# Check centers in MT02
mt02_centers = db.studentrawmarks.distinct("centerId", {"testId": "MT02"})
print(f"Centers in MT02: {mt02_centers}")

