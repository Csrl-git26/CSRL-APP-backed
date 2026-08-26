import os
import pymongo
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv('.env')

mongo_uri = os.environ.get('MONGO_URI')

if not mongo_uri:
    print("MONGO_URI not found in .env")
    exit(1)

client = pymongo.MongoClient(mongo_uri)
db = client.get_default_database()

if db is None:
    # try picking from uri or default to csrl
    db = client['csrl']

profiles = db.profiles

# Find students with no category
empty_cat_students = profiles.find({
    '$or': [
        {'CATEGORY': {'$exists': False}},
        {'CATEGORY': None},
        {'CATEGORY': ''}
    ]
})

print("Students with 'Other / NA' category:")
for s in empty_cat_students:
    print(f"Roll: {s.get('ROLL_KEY')}, Center: {s.get('centerCode')}")

# Also check for 'Pwd' category
pwd_students = profiles.find({
    'CATEGORY': {'$regex': '^pwd$', '$options': 'i'}
})
print("\nStudents with 'Pwd' category:")
for s in pwd_students:
    print(f"Roll: {s.get('ROLL_KEY')}, Center: {s.get('centerCode')}")

client.close()
