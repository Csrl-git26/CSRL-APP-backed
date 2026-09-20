import os

filepath = "/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestRecordsTable.jsx"
with open(filepath, "r") as f:
    content = f.read()

# Replace `{chartData.map((row) => {` with `{[...chartData].reverse().map((row) => {`
content = content.replace("{chartData.map((row) => {", "{[...chartData].reverse().map((row) => {")

with open(filepath, "w") as f:
    f.write(content)

print("Patched TestRecordsTable.jsx")
