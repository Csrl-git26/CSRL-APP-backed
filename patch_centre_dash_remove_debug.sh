#!/bin/bash
FILE="/Users/surya/Desktop/CSRL-APP-frontend/src/components/CentreDashboard.jsx"

# We'll use awk to remove the debug text and ultimate fallback
awk '
BEGIN { skip = 0 }
{
  if ($0 ~ /\/\/ Ultimate fallback if profile is still undefined/) {
    skip = 1
  }
  
  if (skip == 1) {
    if ($0 ~ /};/) {
      skip = 0
    }
    next
  }
  
  if ($0 ~ /DEBUG:/) {
    next
  }

  if ($0 ~ /<StudentProfileView rollKey={viewingStudentId} data={data} onClose={() => setViewingStudentId(null)} \/>/) {
    print "              <StudentProfileView rollKey={viewingStudentId} data={data} onClose={() => setViewingStudentId(null)} />"
    next
  }
  
  print $0
}
' "$FILE" > "${FILE}.tmp"

mv "${FILE}.tmp" "$FILE"
