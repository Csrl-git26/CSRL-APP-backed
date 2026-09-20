import re
import os

files = [
    "/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentDashboard.jsx",
    "/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx",
    "/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx"
]

pattern = r"\{\(\(\) => \{\n\s*if \(\!overallWeakTopicsData.*?\n\s*\}\)\(\)\}"

new_logic = """{(() => {
              if (!overallWeakTopicsData || !overallWeakTopicsData.subjectWise) return 'Loading...';
              const subjectWise = overallWeakTopicsData.subjectWise;
              
              let maxCount = 0;
              let weakestSub = null;
              
              // 1. Find subject with highest number of weak topics
              Object.keys(subjectWise).forEach(sub => {
                const count = subjectWise[sub]?.weak?.length || 0;
                if (count > maxCount) {
                  maxCount = count;
                  weakestSub = sub;
                }
              });
              
              // 2. If no weak topics, find subject with highest number of moderate topics
              let isMed = false;
              if (!weakestSub) {
                Object.keys(subjectWise).forEach(sub => {
                  const count = subjectWise[sub]?.moderate?.length || 0;
                  if (count > maxCount) {
                    maxCount = count;
                    weakestSub = sub;
                    isMed = true;
                  }
                });
              }
              
              if (!weakestSub) return 'None Flagged';
              
              let formatSub = weakestSub.charAt(0) + weakestSub.slice(1).toLowerCase();
              if (formatSub === 'Mathematics') formatSub = 'Math';
              
              return formatSub + (isMed ? ' (Med)' : '');
            })()}"""
            
new_logic_report = new_logic.replace("'Loading...'", "'N/A'")

for filepath in files:
    if not os.path.exists(filepath): continue
    with open(filepath, "r") as f:
        content = f.read()
        
    logic_to_use = new_logic_report if "StudentReportCard.jsx" in filepath else new_logic
    
    # We need to account for indentation
    # Let's just find the match and replace it
    match = re.search(pattern, content, flags=re.DOTALL)
    if match:
        original = match.group(0)
        
        # Get base indentation of the block
        lines = original.split('\n')
        indent = len(lines[0]) - len(lines[0].lstrip())
        indent_str = " " * indent
        
        formatted_new_logic = ""
        for i, line in enumerate(logic_to_use.split('\n')):
            if i == 0:
                formatted_new_logic += line + "\n"
            else:
                # the new_logic is indented with some spaces, let's just strip and add our indent
                formatted_new_logic += indent_str + line.lstrip() + "\n"
                
        formatted_new_logic = formatted_new_logic.rstrip()
        
        content = content.replace(original, formatted_new_logic)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Fixed {filepath}")
    else:
        print(f"Pattern not found in {filepath}")

