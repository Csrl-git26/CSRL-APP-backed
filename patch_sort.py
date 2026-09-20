import re
import os

frontend_file = "/Users/surya/Desktop/CSRL-APP-frontend/src/services/dataService.js"
backend_file = "/Users/surya/Desktop/CSRL-APP-backed/services/analyticsService.js"

sort_function = """export function sortTestRowsChronologically(rows) {
  const parseSequence = (name) => {
    const match = name.match(/^([A-Za-z\-]+)(\d+)(.*)$/);
    if (!match) return null;
    return {
      prefix: match[1].toUpperCase().replace(/[^A-Z]/g, ''),
      num: parseInt(match[2], 10)
    };
  };

  const getLogicalIndex = (seq) => {
    if (!seq) return -1;
    if (seq.prefix === 'MT' || seq.prefix === 'PT') return seq.num * 10;
    if (seq.prefix === 'CMT' || seq.prefix === 'JCT') return seq.num * 20 + 5;
    if (seq.prefix === 'FMT') return 1000 + seq.num * 10;
    return -1;
  };

  return rows.sort((a, b) => {
    const seqA = parseSequence(a.name);
    const seqB = parseSequence(b.name);
    const idxA = getLogicalIndex(seqA);
    const idxB = getLogicalIndex(seqB);

    if (idxA !== -1 && idxB !== -1 && idxA !== idxB) {
      return idxA - idxB;
    }
    return a.name.localeCompare(b.name, undefined, { numeric: true });
  });
}
"""

with open(frontend_file, "r") as f:
    f_content = f.read()

if "export function sortTestRowsChronologically" not in f_content:
    # Append the function at the end
    f_content += "\n" + sort_function
    # Replace the inline sort
    old_sort = """return Object.values(testsMap).sort((a, b) =>
    a.name.localeCompare(b.name, undefined, { numeric: true })
  );"""
    f_content = f_content.replace(old_sort, "return sortTestRowsChronologically(Object.values(testsMap));")
    
    with open(frontend_file, "w") as f:
        f.write(f_content)
    print("Frontend updated")


with open(backend_file, "r") as f:
    b_content = f.read()

if "export function sortTestRowsChronologically" not in b_content:
    b_content += "\n" + sort_function
    old_sort_student = """return Object.values(testsMap).sort((a, b) =>
    a.name.localeCompare(b.name, undefined, { numeric: true })
  );"""
    b_content = b_content.replace(old_sort_student, "return sortTestRowsChronologically(Object.values(testsMap));")

    old_sort_center = """).sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true }));"""
    b_content = b_content.replace(old_sort_center, ");\n  return sortTestRowsChronologically(res);")
    b_content = b_content.replace("return Object.values(testsMap).map(agg => {", "const res = Object.values(testsMap).map(agg => {")

    with open(backend_file, "w") as f:
        f.write(b_content)
    print("Backend updated")

