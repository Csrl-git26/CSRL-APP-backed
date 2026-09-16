import urllib.request
import json

url = "http://localhost:5001/api/analytics/test-insights?testKey=MMT01,MMT02&stream=NEET"
# wait, authenticateToken middleware is there!
# We can't easily hit it without a token.
