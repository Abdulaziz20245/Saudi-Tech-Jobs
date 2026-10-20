"""Find which job-board system a company uses, and save real sample responses.

Tries every supported ATS with a few candidate identifiers and reports which ones return jobs.
Run it on a machine with internet access; it does not touch the database.

Usage:
    uv run python -m collector.discover tabby tamara salla
    uv run python -m collector.discover --save-fixtures foodics
"""

import argparse
import json
from pathlib import Path

from app.config import get_settings
from collector.http import PoliteClient, SourceError
from collector.location import is_saudi
from collector.models import AtsType, CompanyConfig
from collector.sources import ADAPTERS, ashby, greenhouse, lever, workable

FIXTURES_DIR = Path(__file__).resolve().parents[1] / "tests" / "fixtures"

# SmartRecruiters is excluded from blind probing: its identifiers rarely match the brand name.
PROBE_ORDER: list[AtsType] = ["greenhouse", "lever", "ashby", "workable"]
RAW_URLS = {
    "greenhouse": (greenhouse.URL, {"content": "true"}),
    "lever": (lever.URL, {"mode": "json"}),
    "ashby": (ashby.URL, {"includeCompensation": "true"}),
    "workable": (workable.URL, {"details": "true"}),
}


def candidates(name: str) -> list[str]:
    base = name.lower().strip()
    options = [base, base.replace(" ", ""), base.replace(" ", "-")]
    options += [f"{base.replace(' ', '')}{s}" for s in ("hq", "tech", "sa", "ksa", "careers")]
    return list(dict.fromkeys(options))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", nargs="+", help="company names or likely board identifiers")
    parser.add_argument(
        "--save-fixtures",
        action="store_true",
        help="save the raw JSON of each hit under tests/fixtures/<ats>/",
    )
    args = parser.parse_args()
    settings = get_settings()

    with PoliteClient(
        settings.collector_user_agent,
        settings.collector_rate_limit_per_sec,
        settings.collector_timeout_sec,
        max_attempts=1,
    ) as client:
        for name in args.names:
            hits = []
            for ats in PROBE_ORDER:
                for ident in candidates(name):
                    config = CompanyConfig(name=name, slug=ident, ats=ats, id=ident)
                    try:
                        postings = ADAPTERS[ats](client, config)
                    except SourceError:
                        continue
                    if not postings:
                        continue
                    saudi = sum(is_saudi(p) for p in postings)
                    hits.append(
                        f"  {ats:<10} id={ident:<20} {len(postings):>3} jobs, {saudi} in KSA"
                    )
                    if args.save_fixtures:
                        url, params = RAW_URLS[ats]
                        raw = client.get_json(url.format(id=ident), params=params)
                        out = FIXTURES_DIR / ats / f"{ident}.json"
                        out.parent.mkdir(parents=True, exist_ok=True)
                        out.write_text(
                            json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8"
                        )
                        hits.append(f"  saved {out.relative_to(FIXTURES_DIR.parent.parent)}")
                    break
            print(f"{name}:")
            print("\n".join(hits) if hits else "  no public board found (check careers page)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
