import urllib.request
import json
import jwt # pip install PyJWT

# I need the JWT secret from the .env file
with open('.env', 'r') as f:
    env_content = f.read()
    
secret = None
for line in env_content.split('\n'):
    if line.startswith('JWT_SECRET='):
        secret = line.split('=', 1)[1].strip()

if not secret:
    secret = 'secret'

token = jwt.encode({'id': '2601001', 'centerCode': 'KNP', 'role': 'student'}, secret, algorithm='HS256')

url = "https://csrl-app-backed-1.onrender.com/api/analytics/student-chart?rollKey=2601001&centerCode=KNP"
req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        fmt04 = next((x for x in data.get('chartData', []) if x.get('name') == 'FMT04'), None)
        print("FMT04 Response:", json.dumps(fmt04, indent=2))
        print("WeakSubject Response:", data.get('weakSubject'))
except Exception as e:
    print("Error:", e)
    if hasattr(e, 'read'):
        print(e.read().decode())
