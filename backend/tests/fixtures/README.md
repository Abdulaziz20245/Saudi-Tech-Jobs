# Test fixtures

Saved job-board responses used by the collector tests (no network in tests).

- `*/synthetic_*.json`: hand-written samples shaped after each vendor's documented response.
  They keep tests running before real data is saved.
- Real samples: run `uv run python -m collector.discover --save-fixtures <company>` on a machine
  with internet access. Each hit is saved here as `<ats>/<id>.json`; add a test that loads it.
