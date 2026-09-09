import urllib.request
import json

url = "https://csrl-pragati.vercel.app/api/data/student?roll_no=2622013"
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    tests = data.get('tests', {})
    fmt04 = tests.get('FMT04')
    print(json.dumps(fmt04, indent=2))
