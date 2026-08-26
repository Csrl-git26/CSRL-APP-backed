import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx'
with open(filepath, 'r') as f:
    content = f.read()

# Define actualWeakTopics right after actualChart
# I know actualChart is defined somewhere. Let's find it.
if "const actualChart = prefetchedChart || chart;" in content:
    content = content.replace(
        "const actualChart = prefetchedChart || chart;",
        "const actualChart = prefetchedChart || chart;\n  const actualWeakTopics = prefetchedWeakTopics || overallWeakTopicsData;"
    )
    with open(filepath, 'w') as f:
        f.write(content)
    print("Fixed reference error!")
else:
    print("Could not find actualChart definition")
