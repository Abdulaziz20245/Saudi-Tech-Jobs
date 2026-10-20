# Saudi Tech Jobs

AI-powered market intelligence for tech jobs in Saudi Arabia. We collect public job postings
every day, use an LLM to turn each posting into structured data (skills, seniority, salary,
location, work mode), and show the market on a public dashboard. A CV coach agent compares a
user's CV against the live market and recommends what to learn next.

Owner: Abdulaziz (KFUPM CS junior). This is a portfolio project that must have **real users and
measurable results**, so prefer working, deployed, measured features over clever unfinished ones.

## Read these first
- `docs/PRD.md`: who it's for, features, MVP scope, success metrics
- `docs/ARCHITECTURE.md`: components, data model, API, deployment
- `docs/DATA_SOURCES.md`: where jobs come from and the rules for collecting them
- `docs/EXTRACTION_AND_EVALS.md`: LLM extraction schema and how we measure accuracy
- `docs/ROADMAP.md`: milestones and current status (update checkboxes as work lands)
- `docs/DECISIONS.md`: architecture decision records; add an ADR for any significant choice
- `docs/PRIVACY_AND_ETHICS.md`: CV handling, data use, honest presentation rules
- `docs/TESTING.md`: test strategy and quality gates
- `docs/DEPLOYMENT.md`: environments, secrets, workflows, release checklist
- `design/DESIGN_BRIEF.md`: the visual design brief (also given to Claude Design)
- `CONTRIBUTING.md`: branch names, Conventional Commits, PR rules

## Stack
- **Backend / pipeline:** Python 3.12, FastAPI, SQLAlchemy 2 + Alembic, `httpx`, Pydantic v2
- **Database:** PostgreSQL (hosted: Neon or Supabase free tier)
- **LLM:** Anthropic API via the official `anthropic` Python SDK, cheapest capable Claude model
  for extraction, a stronger model for the CV coach agent
- **Frontend:** React + TypeScript + Vite, Tailwind CSS, Recharts for charts
- **Scheduling:** GitHub Actions cron runs the collector and extractor daily
- **Hosting:** frontend on Vercel, API on Render or Fly.io

## Repo layout (target)
```
backend/
  app/            FastAPI app (routers, schemas, services)
  collector/      one module per job source (greenhouse.py, lever.py, ashby.py, workable.py, ...)
  extraction/     LLM extraction prompts, schema, runner
  evals/          labeled dataset + scoring scripts
  db/             models, Alembic migrations
  tests/
frontend/
  src/            pages, components, api client
data/
  companies.yaml  curated list of Saudi tech companies and their job-board identifiers
docs/  design/
```

## Commands (fill in as they become real)
- `cd backend && uv sync` install backend deps
- `uv run pytest` run backend tests
- `uv run python -m collector.run` collect postings
- `uv run python -m extraction.run` extract structured fields for new postings
- `uv run python -m evals.score` score extraction against the labeled set
- `uv run uvicorn app.main:app --reload` run the API locally
- `cd frontend && npm install && npm run dev` run the site locally

## Rules
- **Secrets:** never commit API keys. Read `ANTHROPIC_API_KEY` and `DATABASE_URL` from env;
  keep `.env` in `.gitignore` and provide `.env.example`.
- **Data sources:** only use the public job-board APIs listed in `docs/DATA_SOURCES.md`. Do not
  scrape LinkedIn, Bayt, Indeed, GulfTalent or other sites whose terms forbid it. Identify
  ourselves with a clear User-Agent, respect rate limits (max ~1 request/second per host).
- **Idempotent pipeline:** re-running the collector or extractor must never create duplicates.
  Postings are keyed by `(source, source_job_id)`; extraction is keyed by posting + prompt version.
- **Measure before claiming:** any change to the extraction prompt or schema bumps
  `PROMPT_VERSION` and is re-scored with `evals.score`; record the result in
  `docs/EXTRACTION_AND_EVALS.md`.
- **Bilingual:** postings can be Arabic, English or mixed. Extraction outputs normalized English
  skill names; keep the original text.
- **Cost:** log tokens per extraction run; cache results so a posting is never extracted twice for
  the same prompt version.
- **Style:** type hints everywhere, small modules, tests for every collector (using saved sample
  responses in `tests/fixtures/`, no live network calls in tests).
- Keep the docs current: when a decision changes, update the relevant doc in the same commit.
