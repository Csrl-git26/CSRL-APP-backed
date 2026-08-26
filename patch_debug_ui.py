import re

filepath = '/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx'
with open(filepath, 'r') as f:
    content = f.read()

debug_code = """          <div>
            <h1>Student Profile</h1>
            <p>{profile?.["STUDENT'S NAME"]} &middot; {viewingStudentId}</p>
            <div style={{color:'red', fontSize:10}}>
              DEBUG: data.profiles.length={data?.profiles?.length}, 
              profileByRoll.has(viewingStudentId)={profileByRoll?.has(viewingStudentId) ? 'true' : 'false'},
              has(Number)={profileByRoll?.has(Number(viewingStudentId)) ? 'true' : 'false'},
              has(String)={profileByRoll?.has(String(viewingStudentId)) ? 'true' : 'false'}
            </div>
          </div>"""

content = content.replace("""          <div>
            <h1>Student Profile</h1>
            <p>{profile?.["STUDENT'S NAME"]} · {viewingStudentId}</p>
          </div>""", debug_code)

with open(filepath, 'w') as f:
    f.write(content)
print("Patched UI")
