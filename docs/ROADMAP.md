# Roadmap

Status key: [ ] not started, [~] in progress, [x] done

## Milestone 1: Data pipeline
- [x] Backend scaffold (uv, FastAPI, settings), `.env.example`, CI (lint, types, tests on Postgres)
- [x] Collector adapters for Greenhouse, Lever, Ashby, Workable, SmartRecruiters with tests
- [x] Postgres schema + Alembic migrations, idempotent upserts, closed-posting detection
- [x] KSA location filter (English + Arabic place names, country codes)
- [x] `collector.discover` CLI to find a company's job board and save real fixtures
- [~] Daily GitHub Actions run (workflow ready; enable after production DB exists)
- [ ] Verify ATS endpoints against live data and build `data/companies.yaml` (target 40+)
- [ ] Replace synthetic fixtures with real saved responses
- [ ] Frontend scaffold (Vite) — with Milestone 3

## Milestone 2: Extraction you can measure
- [ ] Extraction schema + prompt v1 with Pydantic validation
- [ ] Skill normalization table with aliases (English + Arabic)
- [ ] Label 200 postings; scoring script; baseline numbers logged
- [ ] Iterate prompt until skills F1 is strong; record every version

## Milestone 3: Launch the website
- [ ] Visual design from Claude Design (see `design/DESIGN_BRIEF.md`)
- [ ] FastAPI read endpoints
- [ ] Dashboard, job explorer, skill pages
- [ ] Deploy (Vercel + Render/Fly + Neon/Supabase), analytics, custom domain (optional)
- [ ] Launch post on LinkedIn with first findings

## Milestone 4: CV coach agent
- [ ] Agent with tools: `search_postings`, `skill_demand`, `compare_skills`
- [ ] CV upload (PDF) + target role → report
- [ ] Rate limiting and cost guard
- [ ] Second LinkedIn post; collect user feedback

## Later ideas
Arabic UI, weekly email digest, non-tech jobs, other GCC countries, public dataset/API.
