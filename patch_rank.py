import re
import os

# 1. Patch analyticsService.js
analytics_path = '/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js'
with open(analytics_path, 'r') as f:
    analytics_content = f.read()

robust_check = """
            const subKey = Object.keys(testDoc).find(tk => {
              if (!tk.startsWith(k)) return false;
              const tkUpper = tk.toUpperCase();
              const subUpper = sub.toUpperCase();
              if (tkUpper.includes(subUpper) || (tkUpper.includes("PHY") && sub === "Physics") || (tkUpper.includes("CHEM") && sub === "Chemistry") || (tkUpper.includes("BIO") && sub === "Biology") || (tkUpper.includes("BOT") && sub === "Botany") || (tkUpper.includes("ZOO") && sub === "Zoology") || (tkUpper.includes("MAT") && sub === "Math") || (tkUpper.includes("MATHS") && sub === "Math")) return true;
              return false;
            });
"""

# Replace the specific line in rankStudentsByTest
old_check = r"const subKey = Object\.keys\(testDoc\)\.find\(tk => tk\.startsWith\(k\) && tk\.toLowerCase\(\)\.includes\(sub\.toLowerCase\(\)\)\);"
analytics_content = re.sub(old_check, robust_check.strip(), analytics_content)

with open(analytics_path, 'w') as f:
    f.write(analytics_content)

# 2. Patch server.js to respect centerCode in test-insights
server_path = '/Users/surya/Desktop/CSRL-APP-backed/server.js'
with open(server_path, 'r') as f:
    server_content = f.read()

test_insights_logic = """
  let resolvedCenterCode = req.query.centerCode;
  if (!resolvedCenterCode || resolvedCenterCode === 'undefined' || resolvedCenterCode === 'null') {
    if (req.user.role === 'centre') {
      resolvedCenterCode = req.user.id;
    } else {
      resolvedCenterCode = '';
    }
  }

  const global = resolvedCenterCode ? await loadCenterApplicationData(resolvedCenterCode) : await loadApplicationData();
"""

old_test_insights = r"const global = await loadApplicationData\(\);"
server_content = re.sub(old_test_insights, test_insights_logic.strip(), server_content, count=1)

with open(server_path, 'w') as f:
    f.write(server_content)

# 3. Patch CentreDashboard.jsx to pass centerCode
centre_path = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(centre_path, 'r') as f:
    centre_content = f.read()

centre_content = re.sub(r"fetchTestInsights\(null, selectedTestKey, null, globalStream\)", "fetchTestInsights(null, selectedTestKey, selectedCenterCode, globalStream)", centre_content)

with open(centre_path, 'w') as f:
    f.write(centre_content)

print("Patch applied successfully.")
