import urllib.request
import json
import traceback

def run():
    try:
        # Assuming the backend is running locally on some port? No, we don't have access to the prod backend.
        # But wait, there's a debug endpoint! /api/debug/student/2616018
        pass
    except Exception as e:
        print(traceback.format_exc())

run()
