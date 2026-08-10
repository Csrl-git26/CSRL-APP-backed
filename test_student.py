import urllib.request
import urllib.parse
import json

url = "https://csrl-app-backed-1.onrender.com/api/auth/login"
data = json.dumps({"role": "student", "id": "2601001"}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode())
        token = res.get('token')
        
        student_url = "https://csrl-app-backed-1.onrender.com/api/students/2601001"
        student_req = urllib.request.Request(student_url, headers={'Authorization': 'Bearer ' + token})
        try:
            with urllib.request.urlopen(student_req) as student_res:
                student_data = json.loads(student_res.read().decode())
                print("STUDENT DATA KEYS:", list(student_data.keys()))
        except Exception as e:
            print("Student Error:", e)
            if hasattr(e, 'read'):
                print(e.read().decode())
except Exception as e:
    print("Login Error:", e)
    if hasattr(e, 'read'):
        print(e.read().decode())
