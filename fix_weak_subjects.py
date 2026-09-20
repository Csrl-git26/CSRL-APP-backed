import os
import re

# We will modify three files in the frontend repository
files_to_fix = [
    "/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentDashboard.jsx",
    "/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentProfileView.jsx",
    "/Users/surya/Desktop/CSRL-APP-frontend/src/components/StudentReportCard.jsx"
]

for filepath in files_to_fix:
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
        
    with open(filepath, "r") as f:
        content = f.read()

    # We need to replace the old overallWeakSubjects logic with overallWeakTopicsData.subjectWise logic
    # First, let's find the exact block for "By Accuracy" loading state
    
    # In StudentDashboard.jsx and StudentProfileView.jsx
    old_logic = """                  if (!overallWeakSubjects) return 'Loading...';
                  const weakest = [];
                  Object.keys(overallWeakSubjects).forEach(sub => {
                    if (overallWeakSubjects[sub]?.strongWeak?.length > 0) weakest.push(sub);
                  });
                  if (weakest.length === 0) {
                    Object.keys(overallWeakSubjects).forEach(sub => {
                      if (overallWeakSubjects[sub]?.mediumWeak?.length > 0) weakest.push(`${sub} (Medium)`);
                    });
                  }
                  return weakest.length > 0 ? weakest.join(', ') : 'None';"""
                  
    new_logic = """                  if (!overallWeakTopicsData || !overallWeakTopicsData.subjectWise) return 'Loading...';
                  const weakest = [];
                  const subjectWise = overallWeakTopicsData.subjectWise;
                  Object.keys(subjectWise).forEach(sub => {
                    const formatSub = sub.charAt(0) + sub.slice(1).toLowerCase();
                    if (subjectWise[sub]?.weak?.length > 0) weakest.push(formatSub);
                  });
                  if (weakest.length === 0) {
                    Object.keys(subjectWise).forEach(sub => {
                      const formatSub = sub.charAt(0) + sub.slice(1).toLowerCase();
                      if (subjectWise[sub]?.moderate?.length > 0) weakest.push(`${formatSub} (Medium)`);
                    });
                  }
                  return weakest.length > 0 ? weakest.join(', ') : 'None';"""
                  
    if old_logic in content:
        content = content.replace(old_logic, new_logic)
        print(f"Replaced By Accuracy block in {filepath}")
    else:
        print(f"Could not find exact block in {filepath}")

    with open(filepath, "w") as f:
        f.write(content)
