import urllib.request
import json

url = "https://csrl-app-backed-1.onrender.com/api/debug-chart/2601001"
req = urllib.request.Request(url)
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        fmt04 = next((x for x in data.get('chartData', []) if x.get('name') == 'FMT04'), None)
        print("DEBUG-CHART FMT04:", json.dumps(fmt04))
except Exception as e:
    print(e)
