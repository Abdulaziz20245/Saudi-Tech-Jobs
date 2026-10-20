# Saudi Tech Jobs

**Live, AI-powered intelligence on the Saudi tech job market.**
See which skills employers are asking for, how demand is changing, what roles pay, and get a
personal plan to close your skill gap.

> Status: in active development. See [docs/ROADMAP.md](docs/ROADMAP.md).

<!-- Add a screenshot / GIF of the dashboard here once deployed -->

## What it does
- **Collects** tech job postings every day from Saudi companies' public job boards
- **Understands** each posting with an LLM: skills, seniority, city, work mode, salary
  (Arabic and English)
- **Measures** its own accuracy against a hand-labeled dataset (see
  [evaluation results](docs/EXTRACTION_AND_EVALS.md#results-log))
- **Shows** the market on a fast public dashboard: top skills, trends, cities, companies, salaries
- **Coaches** you: upload a CV, pick a target role, get your match score, missing skills ranked
  by demand, and matching open jobs

## Tech stack
| Layer | Tools |
|---|---|
| Pipeline & API | Python 3.12, FastAPI, SQLAlchemy 2, Alembic, httpx, Pydantic v2 |
| AI | Anthropic Claude API (structured extraction, tool-using agent) |
| Data | PostgreSQL |
| Frontend | React, TypeScript, Vite, Tailwind CSS, Recharts |
| Ops | GitHub Actions (CI + daily pipeline), Vercel, Render/Fly.io, Neon/Supabase |

## Architecture
```
GitHub Actions (daily) ─► collector ─► PostgreSQL ◄─ extractor ◄─ Claude API
                                          ▲
                         React dashboard ─► FastAPI ─► CV coach agent ─► Claude API
```
Details in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Getting started
Prerequisites: [uv](https://docs.astral.sh/uv/) (installs Python 3.12 for you), Docker for local
Postgres (or a free hosted Postgres such as Neon; put its URL in `.env`).

```bash
git clone https://github.com/Abdulaziz20245/Saudi-Tech-Jobs.git
cd Saudi-Tech-Jobs
cp .env.example .env              # then fill in your values

docker compose up -d db           # local Postgres
cd backend
uv sync                           # install dependencies
uv run alembic upgrade head       # create tables
uv run pytest                     # 36 tests, no network needed
uv run python -m collector.run    # collect postings from data/companies.yaml
uv run uvicorn app.main:app --reload   # API at http://localhost:8000/docs
```

## Documentation
| Doc | What's inside |
|---|---|
| [PRD](docs/PRD.md) | Problem, users, features, success metrics |
| [Architecture](docs/ARCHITECTURE.md) | Components, data model, API |
| [Data sources](docs/DATA_SOURCES.md) | Where data comes from and collection rules |
| [Extraction & evals](docs/EXTRACTION_AND_EVALS.md) | LLM schema and accuracy results |
| [Decisions](docs/DECISIONS.md) | Why things are built the way they are |
| [Privacy & ethics](docs/PRIVACY_AND_ETHICS.md) | CV handling, data use, limitations |
| [Testing](docs/TESTING.md) | Test strategy and how to run tests |
| [Deployment](docs/DEPLOYMENT.md) | Hosting, secrets, scheduled jobs |
| [Roadmap](docs/ROADMAP.md) | Milestones and progress |
| [Design brief](design/DESIGN_BRIEF.md) | Visual design direction |

## Data and disclaimer
Job data comes from employers' public job boards and always links back to the original posting.
Figures are estimates based on collected postings and are not official labor statistics.

## Author
**Abdulaziz Saleh**, Computer Science, KFUPM
[LinkedIn](#) · [GitHub](https://github.com/Abdulaziz20245)

## License
[MIT](LICENSE)
