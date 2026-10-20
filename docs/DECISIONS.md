# Architecture Decision Records

Short records of important decisions: context, decision, consequences. Add a new entry
(never rewrite an old one; mark it "Superseded by ADR-00X" instead).

## ADR-001: Scope to tech jobs in Saudi Arabia first
- **Context:** A focused dataset can launch fast and has a clear audience (our own network).
- **Decision:** Only tech roles located in KSA or remote open to KSA.
- **Consequences:** Smaller volume at first; easy to expand later via the `is_tech` flag and
  more sources.

## ADR-002: Collect from public ATS job-board APIs only
- **Context:** Aggregators (LinkedIn, Bayt, Indeed) have no public API and their terms generally
  forbid scraping. Greenhouse, Lever, Ashby, Workable and SmartRecruiters publish public
  job-board APIs for displaying postings.
- **Decision:** Use those APIs over a curated company list; link back to original postings.
- **Consequences:** Legally clean, structured data; coverage depends on growing the company list.

## ADR-003: LLM extraction with a fixed schema and measured accuracy
- **Context:** Postings are free text in Arabic, English or both; rule-based parsing is brittle.
- **Decision:** Claude with structured output, validated by Pydantic, versioned prompts, and a
  hand-labeled eval set scored on every change.
- **Consequences:** Small per-posting cost (mitigated by caching per prompt version); accuracy is
  a reported number, not a guess.

## ADR-004: Python backend + React frontend
- **Context:** Owner is strongest in Python; the AI ecosystem is Python-first; owner knows React.
- **Decision:** FastAPI + SQLAlchemy + Postgres; React + TypeScript + Vite + Tailwind.
- **Consequences:** Two deployables (API and static site), clear separation of concerns.

## ADR-005: GitHub Actions as the scheduler
- **Context:** The pipeline runs once a day for a few minutes; a dedicated worker is overkill.
- **Decision:** Scheduled GitHub Actions workflow runs collector then extractor.
- **Consequences:** Free and visible; runs are logged in the Actions tab. Revisit if runtime grows.

## ADR-006: Do not store CVs by default
- **Context:** CVs are personal data.
- **Decision:** The CV coach processes CVs in memory and stores only anonymous aggregate events
  (role chosen, match score bucket), unless the user explicitly opts in.
- **Consequences:** No account system needed for MVP; lower privacy risk.
