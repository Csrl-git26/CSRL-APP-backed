from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:YtL8ZtOaJ2sA8E6@csrl-app.2e1i8.mongodb.net/csrl_db?retryWrites=true&w=majority")
db = client.get_database("csrl_db")
student_weak_topics = db.get_collection("studentweaktopics")

topics = list(student_weak_topics.find({"studentId": "2601001"}))
print(f"Found {len(topics)} weak topic docs for 2601001.")
for t in topics:
    print(f"Test ID: {t.get('testId')}, Math Attempted: {t.get('subjectMetrics', {}).get('Mathematics', {}).get('attempted')}")

