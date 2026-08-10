import urllib.request
import json
import jwt

# Get token from csrl-app-backed-1 (NEW BACKEND)
url = "https://csrl-app-backed-1.onrender.com/api/auth/login"
data = json.dumps({"role": "student", "id": "2601001"}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as response:
    res = json.loads(response.read().decode())
    token = res.get('token')
    print("Got token from csrl-app-backed-1")

# Use token on csrl-app-backed-1
student_url = "https://csrl-app-backed-1.onrender.com/api/data/student"
student_req = urllib.request.Request(student_url, headers={'Authorization': 'Bearer ' + token})
try:
    with urllib.request.urlopen(student_req) as student_res:
        student_data = json.loads(student_res.read().decode())
        print("Success hitting csrl-app-backed-1! Keys:", list(student_data.keys()))
except Exception as e:
    print("Error hitting csrl-app-backed-1:", e)
    if hasattr(e, 'read'):
        print(e.read().decode())
