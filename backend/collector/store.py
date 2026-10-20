"""Persist collected postings idempotently.

Postings are keyed by (source, source_job_id). Re-running never duplicates; a posting that
disappears from its company's board gets `closed_at`, and is reopened if it comes back.
"""

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from collector.models import CompanyConfig, RawPosting
from collector.text import content_hash, detect_language
from db.models import Company, Posting


@dataclass
class SyncResult:
    new: int = 0
    updated: int = 0
    closed: int = 0
    unchanged: int = 0


def upsert_company(session: Session, config: CompanyConfig) -> Company:
    company = session.scalar(select(Company).where(Company.slug == config.slug))
    if company is None:
        company = Company(slug=config.slug, name=config.name)
        session.add(company)
    company.name = config.name
    company.website = config.website
    company.ats_type = config.ats
    company.ats_identifier = config.id
    company.active = True
    session.flush()
    return company


def sync_company_postings(
    session: Session, company: Company, postings: list[RawPosting], now: datetime
) -> SyncResult:
    """Upsert the company's current postings and close the ones no longer listed."""
    result = SyncResult()
    existing = {
        (p.source, p.source_job_id): p
        for p in session.scalars(select(Posting).where(Posting.company_id == company.id))
    }
    seen: set[tuple[str, str]] = set()

    for raw in postings:
        key = (raw.source, raw.source_job_id)
        if key in seen:
            continue
        seen.add(key)
        digest = content_hash(raw.title, raw.description_text, raw.location_raw)
        posting = existing.get(key)

        if posting is None:
            posting = Posting(
                company_id=company.id,
                source=raw.source,
                source_job_id=raw.source_job_id,
                first_seen_at=now,
            )
            session.add(posting)
            result.new += 1
        elif posting.content_hash != digest or posting.closed_at is not None:
            result.updated += 1
        else:
            result.unchanged += 1

        posting.title = raw.title[:500]
        posting.description_html = raw.description_html
        posting.description_text = raw.description_text
        posting.language = detect_language(f"{raw.title}\n{raw.description_text}")
        posting.location_raw = raw.location_raw[:500]
        posting.department = raw.department
        posting.employment_type_raw = raw.employment_type_raw
        posting.workplace_type_raw = raw.workplace_type_raw
        posting.apply_url = raw.apply_url
        posting.posted_at = raw.posted_at
        posting.content_hash = digest
        posting.last_seen_at = now
        posting.closed_at = None

    for existing_key, posting in existing.items():
        if existing_key not in seen and posting.closed_at is None:
            posting.closed_at = now
            result.closed += 1

    company.last_collected_at = now
    company.last_error = None
    session.flush()
    return result
