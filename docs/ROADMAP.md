# Roadmap

Status key: [ ] not started, [~] in progress, [x] done

## Milestone 1: Data pipeline
- [ ] Repo scaffold (backend with uv, frontend with Vite), `.env.example`, CI running tests
- [ ] Verify ATS endpoints and build `data/companies.yaml` (target 40+ companies)
- [ ] Collector adapters with fixture-based tests
- [ ] Postgres schema + Alembic migrations, idempotent upserts, closed-posting detection
- [ ] Daily GitHub Actions run

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
