# Architecture

```
 GitHub Actions (daily cron)
   ├─ collector  ── public job-board APIs ──► postings (raw)
   └─ extractor  ── Anthropic API ─────────► posting_extractions (structured)
                                               │
 PostgreSQL ◄──────────────────────────────────┘
   ▲
   │ SQL (read)            HTTPS/JSON
 FastAPI  ◄──────────────────────────── React dashboard (Vercel)
   └─ CV coach agent (Anthropic API + tools over the DB)
```

## Components
1. **Collector** (`backend/collector/`): one adapter per source implementing
   `fetch(company) -> list[RawPosting]`. Reads `data/companies.yaml`, upserts into `postings`,
   marks postings missing from the source as closed (`closed_at`).
2. **Tech filter**: cheap rule-based filter (title keywords) plus LLM confirmation so only tech
   roles reach the dashboard.
3. **Extractor** (`backend/extraction/`): sends title + description to Claude with a strict
   JSON schema (see `EXTRACTION_AND_EVALS.md`), validates with Pydantic, normalizes skills to a
   canonical list (`skills` table, with aliases like "JS" → "JavaScript", "بايثون" → "Python").
4. **API** (`backend/app/`): read-only endpoints for the dashboard, plus the CV coach.
5. **Frontend** (`frontend/`): dashboard, job explorer, skill pages, CV coach.

## Data model (initial)
- `companies`: id, name, slug, website, ats_type, ats_identifier, active, last_collected_at,
  last_error (logo_url, industry later)
- `postings`: id, company_id, source, source_job_id (unique with source), title,
  description_html, description_text, language (en | ar | mixed), location_raw, department,
  employment_type_raw, workplace_type_raw, apply_url, posted_at, first_seen_at, last_seen_at,
  closed_at, content_hash
- `collection_runs`: one row per collector pass (companies ok/failed, postings new/updated/
  closed); feeds monitoring and the "last updated" label
- `posting_extractions`: posting_id, prompt_version, model, is_tech, role_family, seniority,
  city, work_mode, employment_type, salary_min, salary_max, salary_currency,
  years_experience_min, extracted_at, input_tokens, output_tokens
- `skills`: id, name, category (language, framework, cloud, data, tool, soft), aliases[]
- `posting_skills`: posting_id, skill_id, prompt_version, requirement (required | nice_to_have)
- `daily_stats` (materialized view or table): date, role_family, skill_id, active_count

## API (v1, read-only unless noted)
- `GET /api/stats/overview` headline numbers + last updated
- `GET /api/skills/top?role_family=&seniority=&days=30`
- `GET /api/skills/{slug}` skill detail + trend + co-occurring skills
- `GET /api/trends?skills=python,react&days=180`
- `GET /api/postings?q=&role_family=&skill=&city=&seniority=&work_mode=&page=`
- `GET /api/companies` hiring companies with open counts
- `POST /api/coach` CV text or PDF + target role → match report (rate limited)

## Deployment
- Postgres on Neon/Supabase (free tier), connection via `DATABASE_URL`
- API on Render/Fly.io; frontend on Vercel with `VITE_API_URL`
- GitHub Actions secrets: `DATABASE_URL`, `ANTHROPIC_API_KEY`
- Analytics: Plausible or Umami (privacy-friendly, no cookies banner needed)
