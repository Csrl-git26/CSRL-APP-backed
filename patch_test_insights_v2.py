import sys

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestInsightsPanel.jsx'
with open(filepath, 'r') as f:
    content = f.read()

old_logic = """              Total marks criteria: GEN ≥ 110 | EWS ≥ 90 | OBC ≥ 85 | SC ≥ 65 | ST ≥ 60 | PWD ≥ 30.
              Subject-wise criteria: ≥ 20 marks in Physics, Chemistry, and Math across all categories."""

new_logic = """              Total marks criteria: GEN ≥ 110 | EWS ≥ 90 | OBC ≥ 85 | SC ≥ 65 | ST ≥ 60 | PWD ≥ 30."""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched TestInsightsPanel.jsx successfully!")
else:
    print("Could not find the old logic block in TestInsightsPanel.jsx")

