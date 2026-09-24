import pymongo
import os

client = pymongo.MongoClient('mongodb+srv://csrluser:csrllogin2024@csrl-backend.6m649.mongodb.net/csrl_db?retryWrites=true&w=majority&appName=csrl-backend')
db = client['csrl_db']
test_scores = db['testscores']
profiles = db['profiles']

print("Connected to DB.")
tests = list(test_scores.find({"tests.NCT01": {"$exists": True}}))
print("Tests with NCT01 directly:", len(tests))

tests_with_physics = list(test_scores.find({"tests.NCT01_Physics": {"$exists": True}}))
print("Tests with NCT01_Physics directly:", len(tests_with_physics))

tests_with_botany = list(test_scores.find({"tests.NCT01_Botany": {"$exists": True}}))
print("Tests with NCT01_Botany directly:", len(tests_with_botany))

# Fetch all test scores to find any NCT01
all_tests = list(test_scores.find({}))
nct_count = 0
glt_nct_count = 0
for d in all_tests:
    keys = list(d.get('tests', {}).keys())
    neet_keys = [k for k in keys if 'NCT01' in k]
    if neet_keys:
        nct_count += 1
        if d.get('centerCode') == 'GLT':
            glt_nct_count += 1
        elif d.get('tests', {}).get('NCT01', {}).get('centerCode') == 'GLT':
            glt_nct_count += 1

print("Total students with NCT01:", nct_count)
print("GLT students with NCT01:", glt_nct_count)

