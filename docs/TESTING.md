# Testing Strategy

## Backend (pytest)
- **Collector adapters:** each adapter tested against a saved real response in
  `backend/tests/fixtures/<source>/<company>.json`. No live network in tests (use `respx` to mock
  `httpx`). Cover pagination, missing fields, non-KSA filtering.
- **Pipeline idempotency:** running the collector twice on the same fixture produces no
  duplicates; postings missing on the second run get `closed_at`.
- **Extraction:** Pydantic schema validation tests; skill normalization tests (aliases, Arabic
  names, casing). The LLM call itself is mocked in unit tests.
- **API:** FastAPI `TestClient` against a test Postgres database (docker or `testcontainers`),
  seeded with a small fixture dataset.
- **Evals are not unit tests:** `python -m evals.score` calls the real model and is run manually
  or in a separate workflow, never on every push.

## Frontend
- Vitest + React Testing Library for components with logic (filters, charts' data mapping).
- Playwright smoke test: dashboard loads, filter changes chart, job search returns results.

## Quality gates (CI on every PR)
- `ruff check` and `ruff format --check`
- `mypy` (strict on `collector/`, `extraction/`)
- `pytest` with coverage report (target 80% on backend core modules)
- `npm run lint`, `npm run typecheck`, `npm test`

## Commands
```bash
cd backend && uv run pytest -q
cd backend && uv run ruff check . && uv run mypy .
cd frontend && npm run lint && npm run typecheck && npm test
```
