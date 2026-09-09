import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("angle={-45}", "angle={-90}")

# let's add a small dx/dy shift if needed, actually let's just see how -90 textAnchor="end" behaves.
# it should align straight down perfectly in Recharts.
# To be safe and centered nicely under the bar, for -90, Recharts puts the end of the text right at the tick center.
# We might need dx={-4} dy={5} or similar. I'll just change the tick properties to add a little dy to give it space.
content = content.replace(
    "tick={{ fontSize: 11, fill: '#1e293b', fontWeight: 500 }}",
    "tick={{ fontSize: 11, fill: '#1e293b', fontWeight: 500, dy: 4, dx: -4 }}"
)

with open(filepath, 'w') as f:
    f.write(content)
print("Updated XAxis angle to -90")
