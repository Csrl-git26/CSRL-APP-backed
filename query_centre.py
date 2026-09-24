import pymongo
client = pymongo.MongoClient('mongodb+srv://csrluser:csrllogin2024@csrl-backend.6m649.mongodb.net/test?retryWrites=true&w=majority&appName=csrl-backend')
db = client['test']

print("Profiles in CENTRE:", db['profiles'].count_documents({'centerCode': {'$regex': '^centre$', '$options': 'i'}}))
profiles = list(db['profiles'].find({'centerCode': {'$regex': '^centre$', '$options': 'i'}}))
roll_keys = [p.get('ROLL_KEY') for p in profiles if p.get('ROLL_KEY')]

tests = list(db['testscores'].find({'ROLL_KEY': {'$in': roll_keys}}))
print("Test scores for CENTRE profiles:", len(tests))

all_test_keys = set()
for t in tests:
    nested = t.get('tests', {})
    for k in nested.keys():
        all_test_keys.add(k)
        
print("Available tests for CENTRE:", all_test_keys)
