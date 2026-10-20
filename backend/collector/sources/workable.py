"""Workable public widget API (powers embeddable careers pages).

A job open in several cities is listed once per city, all with the same shortcode, so entries
are merged into one posting that carries every location.
"""

from typing import Any

from collector.http import PoliteClient, SourceError
from collector.models import CompanyConfig, RawPosting
from collector.sources._util import join_nonempty, parse_datetime
from collector.text import html_to_text

URL = "https://apply.workable.com/api/v1/widget/accounts/{id}"


def _locations(job: dict[str, Any]) -> list[str]:
    listed = [
        join_nonempty(loc.get("city"), loc.get("region"), loc.get("country"))
        for loc in job.get("locations") or []
        if not loc.get("hidden")
    ]
    return [join_nonempty(job.get("city"), job.get("state"), job.get("country")), *listed]


def _country_codes(job: dict[str, Any]) -> set[str]:
    return {(loc.get("countryCode") or "").upper() for loc in job.get("locations") or []}


def fetch(client: PoliteClient, company: CompanyConfig) -> list[RawPosting]:
    data = client.get_json(URL.format(id=company.id), params={"details": "true"})
    if not isinstance(data, dict) or not isinstance(data.get("jobs"), list):
        raise SourceError(f"workable/{company.id}: unexpected response shape")

    grouped: dict[str, list[dict[str, Any]]] = {}
    for job in data["jobs"]:
        key = str(job.get("shortcode") or job.get("code") or job.get("url") or "")
        if key:
            grouped.setdefault(key, []).append(job)

    postings = []
    for shortcode, entries in grouped.items():
        job = entries[0]
        locations = list(dict.fromkeys(loc for e in entries for loc in _locations(e) if loc))
        codes = set().union(*(_country_codes(e) for e in entries))
        description_html = job.get("description")
        postings.append(
            RawPosting(
                source="workable",
                source_job_id=shortcode,
                title=(job.get("title") or "").strip(),
                apply_url=job.get("url") or job.get("shortlink") or "",
                location_raw=" | ".join(locations),
                description_html=description_html,
                description_text=html_to_text(description_html),
                department=job.get("department") or None,
                employment_type_raw=job.get("employment_type") or None,
                workplace_type_raw="Remote" if job.get("telecommuting") else None,
                country_code="SA" if "SA" in codes else None,
                posted_at=parse_datetime(job.get("published_on") or job.get("created_at")),
            )
        )
    return postings
