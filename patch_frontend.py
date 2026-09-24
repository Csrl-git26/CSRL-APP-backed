import os
filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestInsightsPanel.jsx'
try:
    with open(filepath, 'r') as f:
        content = f.read()
    print("Success reading")
except Exception as e:
    print(f"Error: {e}")
