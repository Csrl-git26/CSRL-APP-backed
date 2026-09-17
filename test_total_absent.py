import pymongo

client = pymongo.MongoClient('mongodb+srv://surya:qIqg2X2a537fK63s@csrl.6dhyi.mongodb.net/csrl_db?retryWrites=true&w=majority')
db = client['csrl_db']
t = db['testscores'].find_one({"ROLL_KEY": "2722001"})

if t and 'tests' in t:
    for k, v in t['tests'].items():
        if 'CMT' in k:
            print(f"Test: {k}")
            print(v)
            print("-" * 20)
