import pymongo
import os

client = pymongo.MongoClient('mongodb+srv://csrluser:csrllogin2024@csrl-backend.6m649.mongodb.net/csrl_db?retryWrites=true&w=majority&appName=csrl-backend')
db = client['csrl_db']
test_scores = db['testscores']

print("Connected to DB.")
for d in test_scores.find({}):
    keys = list(d.keys())
    neet_keys = [k for k in keys if k.startswith('NCT')]
    if neet_keys:
        print("NEET KEYS FOUND:")
        for nk in neet_keys:
            print(f"{nk}: {d[nk]}")
        break
