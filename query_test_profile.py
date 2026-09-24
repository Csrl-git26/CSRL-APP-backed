import pymongo
client = pymongo.MongoClient('mongodb+srv://csrluser:csrllogin2024@csrl-backend.6m649.mongodb.net/test?retryWrites=true&w=majority&appName=csrl-backend')
db = client['test']
profile = db['profiles']
neet = profile.find_one({"STREAM": {"$regex": "neet", "$options": "i"}})
jee = profile.find_one({"STREAM": {"$regex": "jee", "$options": "i"}})
print("NEET KEYS:", neet.keys() if neet else "None")
print("JEE KEYS:", jee.keys() if jee else "None")
if neet:
    print("NEET STREAM:", neet.get("STREAM"), "COURSE:", neet.get("COURSE"))
if jee:
    print("JEE STREAM:", jee.get("STREAM"), "COURSE:", jee.get("COURSE"))
