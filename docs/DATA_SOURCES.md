# Data Sources

## Approach
Collect jobs directly from companies' own hiring systems (ATS). These vendors publish free,
unauthenticated job-board APIs meant for displaying a company's open roles elsewhere, which
keeps us clean legally and gives structured data.

| ATS | Endpoint (per company) | Notes |
|---|---|---|
| Greenhouse | `https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true` | No salary or employment type |
| Lever | `https://api.lever.co/v0/postings/{slug}?mode=json` | EU variant `api.eu.lever.co`; ~1 req/s |
| Ashby | `https://api.ashbyhq.com/posting-api/job-board/{name}?includeCompensation=true` | Salary when the employer opts in |
| Workable | `https://apply.workable.com/api/v1/widget/accounts/{account}` | e.g. Foodics → `foodics` |
| SmartRecruiters | `https://api.smartrecruiters.com/v1/companies/{id}/postings` | Paginated |

Endpoints are from vendor docs and public references; verify each one against a real company
before relying on it, and save a sample response to `backend/tests/fixtures/`.

## Company list
`data/companies.yaml` is the curated list of Saudi (or Saudi-hiring) tech employers:
```yaml
- name: Foodics
  ats: workable
  id: foodics
  website: https://www.foodics.com
```
Candidates to check (ATS unknown until verified): Tabby, Tamara, Salla, Zid, Lean Technologies,
Jahez, Foodics (Workable, confirmed), Unifonic, Mozn, Lucidya, Sary, Nana, Ninja, HALA, Rewaa,
Barq, Tweeq, Careem (KSA roles), plus regional and global companies hiring in Riyadh/Jeddah/
Khobar. Find a company's ATS from the URL its "Apply" buttons use.

Only keep postings located in Saudi Arabia (or remote open to KSA).

## Not allowed
Do not scrape LinkedIn, Bayt, Indeed, GulfTalent, Naukrigulf or similar aggregators: no public
API and their terms generally forbid automated collection. Jadarat (national platform) has no
public API that we found. Revisit only with written permission or an official API.

## Etiquette
- User-Agent: `SaudiTechJobsBot/0.1 (+<project URL>)`
- At most ~1 request/second per host, one full pass per day
- Store the source `apply_url` and always link users back to it
