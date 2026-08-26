#!/bin/bash
FILE="/Users/surya/Desktop/CSRL-APP-frontend/src/components/TestRecordsTable.jsx"

# We will use awk to replace the lines
awk '
BEGIN { in_block = 0 }
{
  if ($0 ~ /const stats = calculateSubjectStats\(s\);/) {
    print "                    const stats = calculateSubjectStats(s);"
    print "                    const isTotal = s === \x27Total\x27;"
    in_block = 1
  } else if (in_block == 1 && $0 ~ /{!\isCentre && stats.fails > 0 && \(/) {
    print "                          {!isCentre && !isTotal && stats.fails > 0 && ("
  } else if (in_block == 1 && $0 ~ /{!\isCentre && stats.fails === 0 && stats.avg !== \x27—\x27 && \(/) {
    print "                          {!isCentre && !isTotal && stats.fails === 0 && stats.avg !== \x27—\x27 && ("
  } else {
    print $0
  }
}
' "$FILE" > "${FILE}.tmp"

mv "${FILE}.tmp" "$FILE"
