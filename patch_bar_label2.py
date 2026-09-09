import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreLeaderboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_code = """    const showInside = height > 70;
    
    // Positioning logic:
    // If text is inside, put text at y+20. Put dot ABOVE the bar (y-12)
    // If text is outside, put text at y-10. Put dot ABOVE the text (y-30)
    const textY = showInside ? y + 20 : y - 10;
    const dotY = showInside ? y - 12 : y - 30;
    
    const textColor = showInside ? "#ffffff" : "#1e293b";"""

new_code = """    // ALWAYS show text outside (above) the bar to prevent horizontal cropping
    // on narrow bars.
    const textY = y - 10;
    const dotY = y - 32;
    
    const textColor = "#1e293b";"""

content = content.replace(old_code, new_code)

# Let's also remove fontWeight 600 and make it 500 so it's even thinner and cleaner.
# And font size 10 to be safe.
old_text = 'fontSize={11} fontWeight={600} letterSpacing={-0.5}'
new_text = 'fontSize={10} fontWeight={500} letterSpacing={0}'
content = content.replace(old_text, new_text)

with open(filepath, 'w') as f:
    f.write(content)
print("Updated label positions to always be outside the bar in CentreLeaderboard.jsx")
