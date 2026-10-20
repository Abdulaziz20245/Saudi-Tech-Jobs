# Privacy and Ethics

## Job data
- Collected only from employers' public job-board APIs (see `DATA_SOURCES.md`).
- We store posting text to extract structured data and always link to the original posting.
- Companies can ask to be removed; honor requests within 7 days (`companies.active = false`
  and hide their postings). Contact address goes in the site footer.

## CVs (CV coach)
- Processed in memory and sent to the Anthropic API only to produce the report.
- Not stored, not used to train anything, not shared. Only anonymous aggregates are logged
  (target role, score bucket, timestamp).
- File limits: PDF or text, max 5 MB; reject other types.
- Show a clear notice before upload: what happens to the CV and that it is not stored.
- Note: Anthropic's API data handling terms apply to the request; link them on the About page.

## Analytics
Privacy-friendly analytics (Plausible or Umami): no cookies, no personal identifiers.

## Honest presentation
- Every chart shows its sample size and "last updated" time.
- Salary figures appear only when at least 5 postings state a salary for that slice.
- The methodology page explains coverage limits: we see only companies on our list, so numbers
  describe our sample, not the whole Saudi market.
- Accuracy figures on the site come from the eval log, never rounded up.

## Security
- Secrets only in environment variables / deployment secrets.
- API is read-only except `POST /api/coach`, which is rate limited and size limited.
- Dependencies kept updated (Dependabot); no user accounts in MVP.
