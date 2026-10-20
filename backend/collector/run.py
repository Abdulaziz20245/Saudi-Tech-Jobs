"""Collect postings from every company in data/companies.yaml.

Usage:
    uv run python -m collector.run                 # all companies with a known ATS
    uv run python -m collector.run --only foodics  # one company (by slug)
    uv run python -m collector.run --verified-only
"""

import argparse
import logging
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.config import get_settings
from collector.companies import load_companies
from collector.http import PoliteClient, SourceError
from collector.location import is_saudi
from collector.models import CompanyConfig
from collector.sources import ADAPTERS
from collector.store import sync_company_postings, upsert_company
from db.models import CollectionRun
from db.session import get_sessionmaker

log = logging.getLogger("collector")


def collect(
    session: Session, client: PoliteClient, companies: list[CompanyConfig]
) -> CollectionRun:
    run = CollectionRun(started_at=datetime.now(UTC))
    session.add(run)

    for config in companies:
        company = upsert_company(session, config)
        try:
            raw = ADAPTERS[config.ats](client, config)
        except (SourceError, KeyError, TypeError, AttributeError) as exc:
            # One broken board must not stop the run; keep its postings open until it recovers.
            company.last_error = str(exc)[:2000]
            run.companies_failed += 1
            log.warning("%-24s FAILED  %s", config.slug, exc)
            session.commit()
            continue

        saudi = [p for p in raw if is_saudi(p)]
        result = sync_company_postings(session, company, saudi, datetime.now(UTC))
        run.companies_ok += 1
        run.postings_new += result.new
        run.postings_updated += result.updated
        run.postings_closed += result.closed
        log.info(
            "%-24s %3d listed, %3d in KSA: +%d new, %d updated, %d closed",
            config.slug,
            len(raw),
            len(saudi),
            result.new,
            result.updated,
            result.closed,
        )
        session.commit()

    run.finished_at = datetime.now(UTC)
    session.commit()
    return run


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", help="collect a single company by slug")
    parser.add_argument("--verified-only", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    settings = get_settings()
    companies = load_companies(settings.companies_file, include_unverified=not args.verified_only)
    if args.only:
        companies = [c for c in companies if c.slug == args.only]
    if not companies:
        log.error("No companies to collect. Check data/companies.yaml (ats + id).")
        return 1

    with (
        PoliteClient(
            settings.collector_user_agent,
            settings.collector_rate_limit_per_sec,
            settings.collector_timeout_sec,
        ) as client,
        get_sessionmaker()() as session,
    ):
        run = collect(session, client, companies)

    log.info(
        "Done: %d companies ok, %d failed | %d new, %d updated, %d closed",
        run.companies_ok,
        run.companies_failed,
        run.postings_new,
        run.postings_updated,
        run.postings_closed,
    )
    return 0 if run.companies_ok > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
