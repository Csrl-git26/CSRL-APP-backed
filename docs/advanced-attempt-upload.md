# JEE Advanced attempt-count uploads

Admin → select JEE / Advanced → Import Excel → **JEE Advanced — Attempt & Accuracy Sheet**.

Choose an existing Advanced test, choose an Excel/CSV file, preview its counts and confirm upload. Re-upload replaces the selected test's entire attempt-count snapshot atomically. A version check prevents overwriting a newer upload without previewing it first. No student marks, ranks, Main data or NEET data are modified.

Use the first worksheet with these headers:
`name`, `Roll Number`, `stream`, `centre`, `total_questions`, `not_attempted`, `attempted`, `incorrect`, `correct`, `ACC%` (optional).

Every student must match one existing JEE profile by roll number and centre. Duplicate rolls, unknown profiles, missing counts, negative/fractional counts, and inconsistent counts block the whole upload. Blank trailing rows are ignored. Fix the reported rows and preview again. No partial upload is performed.

Each row must satisfy:
- attempted + not_attempted = total_questions
- correct + incorrect = attempted
- ACC%, if supplied, agrees with correct / attempted × 100 (allowing display rounding).

Question totals may differ between students. The preview flags this and preserves the original counts. A zero-attempt student has 0% accuracy.

Calculations:
- Student attempt: uploaded attempted count.
- Student accuracy: correct / attempted × 100.
- Centre/overall attempt: sum(attempted) / number of uploaded student records in scope.
- Centre/overall accuracy: sum(correct) / sum(attempted) × 100.
- Multiple-test summaries pool the uploaded student-test records.

This format contains total counts only. Subject-wise attempt, correct/wrong counts and accuracy are unavailable, rather than inferred from awarded marks. Student and centre charts, the qualification popup/Excel and notification reports use the Advanced source. Missing Advanced counts remain unavailable. Marks and ranks continue to use existing results. Main and NEET retain their existing behavior.

Data is stored in the separate AdvancedAttemptSheet MongoDB collection, one atomic snapshot per test. The upload is restricted to Admin and tests registered as JEE Advanced. It does not register or reclassify tests. Upload the selected test's results under Advanced first.

After an upload, reopen the relevant Advanced dashboard to refresh its charts. This feature does not import the example attachment automatically because its test ID is not present in the sheet.

Verification: `node --test tests/advancedAttempts.test.js tests/resultNotifications.test.js`; frontend `npm run build`. Tests use synthetic profiles and mocked persistence; the supplied workbook was also checked with the parser without writing production data.
