# Deployment

## Environments
| | Local | Production |
|---|---|---|
| Database | Postgres via `docker compose` | Neon or Supabase (free tier) |
| API | `uvicorn --reload` | Render or Fly.io (Docker image from `backend/Dockerfile`) |
| Frontend | `npm run dev` | Vercel (root: `frontend/`) |
| Pipeline | manual `python -m collector.run` | GitHub Actions cron, daily 03:00 Riyadh (00:00 UTC) |

## Secrets
| Name | Where |
|---|---|
| `DATABASE_URL` | Render/Fly env, GitHub Actions secrets |
| `ANTHROPIC_API_KEY` | Render/Fly env (coach), GitHub Actions secrets (extraction) |
| `VITE_API_URL` | Vercel env |
| `CORS_ORIGINS` | Render/Fly env (the Vercel domain) |

## Workflows (`.github/workflows/`)
- `ci.yml`: lint, typecheck, tests on every push and PR
- `pipeline.yml`: scheduled daily + manual trigger; runs migrations check, collector, extractor,
  refreshes `daily_stats`; fails loudly (and opens an issue) if a source errors repeatedly
- `evals.yml`: manual trigger only; runs the eval set and uploads the report as an artifact

## Release checklist
1. CI green on `main`
2. `alembic upgrade head` on production DB
3. Deploy API, check `GET /api/health`
4. Deploy frontend, check dashboard loads with real data
5. Update `CHANGELOG.md`

## Cost guardrails
- `EXTRACTION_MAX_DAILY_COST_USD` stops extraction when the daily estimate is reached
- Coach endpoint rate limited per IP; set a monthly spend limit in the Anthropic console
