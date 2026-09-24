import re

admin_path = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/AdminDashboard.jsx'
with open(admin_path, 'r') as f:
    admin_content = f.read()

admin_content = re.sub(r"return \['ALL_FMT', \.\.\.sorted\];", "return sorted;", admin_content)
admin_content = re.sub(r"return globalStream === 'NEET' \? sorted : \['ALL_FMT', \.\.\.sorted\];", "return sorted;", admin_content)

with open(admin_path, 'w') as f:
    f.write(admin_content)

centre_path = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(centre_path, 'r') as f:
    centre_content = f.read()

centre_content = re.sub(r"return \['ALL_FMT', \.\.\.cols\];", "return cols;", centre_content)
centre_content = re.sub(r"return globalStream === 'NEET' \? sorted : \['ALL_FMT', \.\.\.sorted\];", "return sorted;", centre_content)

with open(centre_path, 'w') as f:
    f.write(centre_content)

print("Patched successfully")
