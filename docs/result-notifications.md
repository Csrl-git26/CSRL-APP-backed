# Result-release emails — प्रगति

The new **Send Result Notification — प्रगति** card is on Admin → Import Excel.
Existing dashboard tabs, uploads, analytics endpoints and student records are unchanged.

## One-time setup

1. In Resend, add and verify **csrl.in** using the DNS records Resend provides. Ask the domain administrator to add the records. Do not replace existing mail records indiscriminately.
2. Create a Resend sending API key for that verified domain.
3. On the Render backend service, set these environment variables privately:
   - `RESEND_API_KEY`: the Resend API key
   - `RESULT_EMAIL_ENABLED`: `true`
4. Save and redeploy the backend. The sender is fixed as **प्रगति <ajaya.kumar@csrl.in>**.

Do not put the API key in GitHub, frontend environment variables, or chat. The mailbox password is not needed. Without both variables, the card supports previews and downloads but cannot send. The sender must be authorized through domain verification; entering an address alone does not grant sending permission.

Official provider documentation:
- https://resend.com/docs/dashboard/domains/introduction
- https://resend.com/docs/api-reference/emails/send-email
- https://resend.com/docs/dashboard/emails/idempotency-keys

## Admin workflow

1. Choose the portal stream / JEE branch as usual, then open Import Excel.
2. In the new card, select a saved test, its date, and recipients: all, centre users, or CSRL Management users.
3. Click **Preview email & report**. Review the message, centre analysis, recipient list and Excel download.
4. Resolve any report warnings. Question-wise marks and result-sheet counts/averages must agree; subject data must be present.
5. Tick the review checkbox and click **Send notification**, then confirm the recipient count.
6. View progress in Recent notifications. Failed recipients can be retried; accepted recipients are not resent.

Recipients come from the existing active Centre/Management user directory. Non-email user IDs are listed as excluded. Addresses present in both groups receive one email. Users deleted before processing are skipped. No student contact details are taken from student profiles. Each recipient gets an individual email; other recipients' addresses are not exposed.

The email contains the selected test and date, portal link, centre analysis with grouped red headers and OVERALL row, an Excel copy, and an automatically-generated/no-reply footer. JEE uses Physics/Chemistry/Mathematics; NEET uses Physics/Chemistry/Botany/Zoology. Average marks, attempts and accuracy use one decimal. Overall averages are student weighted; accuracy follows existing pooled question-wise calculations. No existing analytics are changed.

## Sending and recovery

A MongoDB outbox stores the exact preview and recipients. Closing the Admin page does not cancel a queued notification. Processing resumes after a backend restart. A sleeping Render instance pauses processing until it wakes; continuous processing requires the backend to remain running.

**Accepted** means Resend accepted the request, not confirmed inbox delivery. Check Resend logs for delivery, bounces and provider limits. No delivery webhook is installed by this feature.

Repeated previews of the same data reuse the same notification. Queueing is atomic, recipients use MongoDB leases, and provider requests use stable idempotency keys. Accepted recipients are never retried. Retries older than 23 hours are placed in **Needs review**, because Resend's idempotency window is 24 hours. Check provider logs before deciding to send a new notification. Do not create changed previews merely to bypass that protection.

A new preview after results, date, scope or audience change creates a separate notification and can email overlapping recipients again after explicit confirmation. History retains the latest 20 notifications in the UI; older records remain in MongoDB.

## Verification

- `node --test tests/resultNotifications.test.js`
- Frontend: `npm run build`

Automated tests mock the provider and database operations. No actual email is sent by the tests.
