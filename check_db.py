import pymongo

URI = "mongodb+srv://surya:qIqg2X2a537fK63s@csrl.6dhyi.mongodb.net/csrl_db?retryWrites=true&w=majority"
client = pymongo.MongoClient(URI)
db = client.get_database("csrl_db")

center_doc = db.centeroverallweaktopics.find_one({"centerId": "GAIL"})
if center_doc:
    print("Center strong:", center_doc.get("subjectWise", {}).get("PHYSICS", {}).get("strong", [])[:3])
else:
    print("Center GAIL not found")

student_doc = db.studentoverallweaktopics.find_one()
if student_doc:
    print("Student strong:", student_doc.get("subjectWise", {}).get("PHYSICS", {}).get("strong", [])[:3])
else:
    print("No student docs")

