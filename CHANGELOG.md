# Changelog

All notable changes to this project are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]
### Added
- Backend scaffold: uv project, settings, SQLAlchemy models, Alembic initial migration,
  FastAPI app with `/api/health`
- Job collector with adapters for Greenhouse, Lever, Ashby, Workable and SmartRecruiters,
  a polite HTTP client (User-Agent, per-host rate limit, retries), KSA location filter,
  idempotent storage with closed-posting detection, and run history
- `collector.discover` CLI to find companies' job boards and save real fixtures
- 36 tests (fixtures, no network), ruff + mypy strict, CI on Postgres, daily pipeline workflow
- `docker-compose.yml` for local Postgres
- Project documentation: PRD, architecture, data sources, extraction and evals, decisions,
  privacy and ethics, testing, deployment, roadmap
- Design brief for the website
- Repository setup: README, license, `.gitignore`, `.env.example`, GitHub templates
