import os
import pymongo
from urllib.parse import urlparse

uri = os.environ.get('MONGO_URI') or open('.env').read().split('MONGO_URI=')[1].split('\n')[0]
parsed = urlparse(uri)
db_name = parsed.path.lstrip('/') if parsed.path else 'test'

client = pymongo.MongoClient(uri)
db = client[db_name]

profile_centers = db.profiles.distinct('centerCode')
marks_centers = db.studentrawmarks.distinct('centerId')

print("Profile Centers (from Excel):", sorted(profile_centers))
print("Marks Centers (from MT01):", sorted(marks_centers))
