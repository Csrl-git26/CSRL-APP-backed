import os

filepath = "/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentDashboard.jsx"
with open(filepath, "r") as f:
    content = f.read()

# Replace `{chartData.map((row) => {` in the table
# We only want to replace the one inside MarksTab.
# To be safe, let's do a precise string replacement on the line that maps chartData in the table body.
content = content.replace("<tbody>\n            {chartData.map((row) => {", "<tbody>\n            {[...chartData].reverse().map((row) => {")

with open(filepath, "w") as f:
    f.write(content)

print("Patched StudentDashboard.jsx table")
