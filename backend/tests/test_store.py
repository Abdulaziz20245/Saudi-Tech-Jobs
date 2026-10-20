from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select

from collector.models import CompanyConfig, RawPosting
from collector.store import sync_company_postings, upsert_company
from db.models import Posting

T0 = datetime(2026, 10, 20, tzinfo=UTC)
CONFIG = CompanyConfig(name="Foodics", slug="foodics", ats="workable", id="foodics")


def raw(job_id, title="Data Engineer", description="Python, SQL"):
    return RawPosting(
        source="workable",
        source_job_id=job_id,
        title=title,
        apply_url=f"https://x/{job_id}",
        location_raw="Riyadh",
        description_text=description,
    )


def count(session):
    return session.scalar(select(func.count()).select_from(Posting))


def test_rerun_does_not_duplicate(session):
    company = upsert_company(session, CONFIG)
    first = sync_company_postings(session, company, [raw("1"), raw("2")], T0)
    second = sync_company_postings(session, company, [raw("1"), raw("2")], T0 + timedelta(days=1))

    assert (first.new, second.new, second.unchanged) == (2, 0, 2)
    assert count(session) == 2


def test_duplicate_ids_in_one_response_are_ignored(session):
    company = upsert_company(session, CONFIG)
    result = sync_company_postings(session, company, [raw("1"), raw("1")], T0)
    assert result.new == 1 and count(session) == 1


def test_missing_postings_close_and_reopen(session):
    company = upsert_company(session, CONFIG)
    sync_company_postings(session, company, [raw("1"), raw("2")], T0)

    closed = sync_company_postings(session, company, [raw("1")], T0 + timedelta(days=1))
    gone = session.scalar(select(Posting).where(Posting.source_job_id == "2"))
    assert closed.closed == 1 and gone.closed_at is not None

    back = sync_company_postings(session, company, [raw("1"), raw("2")], T0 + timedelta(days=2))
    session.refresh(gone)
    assert back.updated == 1 and gone.closed_at is None


def test_content_change_counts_as_update(session):
    company = upsert_company(session, CONFIG)
    sync_company_postings(session, company, [raw("1")], T0)
    result = sync_company_postings(session, company, [raw("1", description="Python, Spark")], T0)
    posting = session.scalar(select(Posting))

    assert result.updated == 1
    assert posting.description_text == "Python, Spark"
    assert posting.first_seen_at.replace(tzinfo=UTC) == T0


def test_upsert_company_is_idempotent(session):
    a = upsert_company(session, CONFIG)
    b = upsert_company(session, CONFIG)
    assert a.id == b.id
