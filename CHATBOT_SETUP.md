# Ask प्रगति

Read-only chat uses the portal's existing profiles and test scores. Existing tabs and result routes are unchanged. The new authenticated endpoints are GET /api/chat/status and POST /api/chat.

## Activate free AI

1. Use a Cloudflare Workers **Free** account. Do not enable paid billing for this pilot.
2. Open Workers AI → Use REST API → Create a Workers AI API Token. Copy the account ID and restricted token.
3. In the Render backend service's Environment settings, add `CLOUDFLARE_ACCOUNT_ID` and secret `CLOUDFLARE_AI_TOKEN`. Save and redeploy. Never add them to Vercel/frontend variables or commit them.
4. Open Ask प्रगति; status should show AI connected. Try the supported questions below and verify the interpretation and table against the marksheet.

Uses the fixed free-eligible model @cf/meta/llama-3.1-8b-instruct-fp8-fast. Cloudflare's current free allocation is 10,000 neurons/day (not messages); provider limits and availability can change. The backend reserves at most 200 model calls/day in MongoDB, limits each response to 500 tokens, and limits each login to 6 requests/minute per process. Provider errors/timeouts and daily limits fall back to database answers. The application ceiling is not a billing guarantee on a paid provider account; keep the provider on Free.

Without these environment variables, supported English questions work through a deterministic parser and calculated summaries. The UI explicitly labels this Database answers mode. Flexible AI understanding and AI explanations are not active until credentials are configured.

## First supported questions

- Which centres improved in the last 2 CMT tests?
- Which centres continuously improved in the last 3 CMT tests?
- KNP centre students needing special attention in Physics in the last 3 CMT tests.
- KNP Physics students below 40 marks in the last 3 CMT tests.
- Student progress roll KNP001 at KNP in Physics, last 3 CMT tests.
- Follow-up: Show only declining students.

Choose stream and JEE branch in chat. Plans can select 1–10 tests of one series. Test numbering determines order; dates are not inferred. No mixing of JEE/NEET or Main/Advanced. Comparisons are raw marks, so same maximum marks/scoring scale must be checked. Centre averages use the same cohort across every selected test; participation counts are displayed separately. Two tests show one change, not repeated improvement.

Default attention rule: latest mark below the centre subject average OR a decline at every step across at least 3 selected tests. The answer states this rule; it is not an official qualification cutoff. Explicit raw-mark thresholds override the below-average rule. Missing/absent/invalid marks are excluded, not treated as zero. Results display at most 200 rows with the full match count.

## Access and data handling

Existing authentication middleware verifies active accounts. Management can analyse all centres; named centre accounts can analyse exact assigned codes only; students can retrieve only their own centre+roll record. Legacy shared centre logins without an assignment are refused by chat. Unresolved assignment labels do not grant access. Student identities join on centre AND roll, never roll alone.

AI receives the user question, permitted centre/test identifiers and previous validated filters. Explanation prompts receive aggregate result text and criteria, without student rows, names, roll numbers or full profiles. A user may include personal data in their own question; the chat UI discloses external processing. No chat transcript is persisted. A Mongo collection chat_ai_daily_usage holds only UTC date and model-call count. No arbitrary model-generated database queries or mutations are executed. Unsupported metrics (qualification rates, ranks, attendance, faculty ratings, causes) request clarification instead of substituting averages.

## Validation

Run `node --experimental-vm-modules --test tests/chatAnalysis.test.js tests/chatRoute.test.js`. No credentials or live student records are required. Deployment still needs a real-account smoke test for provider access, role assignments and current imported marks.
