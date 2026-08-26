import sys

with open('/Users/surya/.gemini/antigravity-ide/brain/567b3099-b6f3-42e8-b895-bacad9ca8f38/task.md', 'w') as f:
    f.write("""- `[ ]` Update `StudentReportCard.jsx` to accept an optional `idSuffix` or `containerId` prop for unique DOM IDs.
- `[ ]` Update `CentreDashboard.jsx` to import `jsPDF` and `html2canvas`.
- `[ ]` Add state for `isExportingBulk` and `bulkExportProgress` in `CentreDashboard.jsx`.
- `[ ]` Create a hidden container in `CentreDashboard.jsx` that mounts `StudentReportCard` for all filtered students when `isExportingBulk` is true.
- `[ ]` Write the `handleExportAllPDFs` function to iterate through the filtered students, capture each container, add a page to `jsPDF`, and save the file.
- `[ ]` Add the "Export All to PDF" button in the `StudentsSection` header.
- `[ ]` Test and verify layout and progress indication.
""")

