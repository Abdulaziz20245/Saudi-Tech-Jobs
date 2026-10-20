"""SmartRecruiters Posting API: https://developers.smartrecruiters.com/docs/posting-api

The list endpoint has no description, so each Saudi posting costs one extra request.
"""

from typing import Any

from collector.http import PoliteClient, SourceError
from collector.models import CompanyConfig, RawPosting
from collector.sources._util import join_nonempty, parse_datetime
from collector.text import html_to_text

LIST_URL = "https://api.smartrecruiters.com/v1/companies/{id}/postings"
DETAIL_URL = "https://api.smartrecruiters.com/v1/companies/{id}/postings/{posting_id}"
PAGE_SIZE = 100
MAX_PAGES = 20


def _list_saudi_postings(client: PoliteClient, company: CompanyConfig) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for page in range(MAX_PAGES):
        data = client.get_json(
            LIST_URL.format(id=company.id),
            params={"limit": PAGE_SIZE, "offset": page * PAGE_SIZE, "country": "sa"},
        )
        if not isinstance(data, dict) or not isinstance(data.get("content"), list):
            raise SourceError(f"smartrecruiters/{company.id}: unexpected response shape")
        items.extend(data["content"])
        if len(items) >= int(data.get("totalFound") or 0) or not data["content"]:
            break
    return items


def fetch(client: PoliteClient, company: CompanyConfig) -> list[RawPosting]:
    postings = []
    for item in _list_saudi_postings(client, company):
        detail = client.get_json(DETAIL_URL.format(id=company.id, posting_id=item["id"]))
        sections = ((detail.get("jobAd") or {}).get("sections") or {}) if detail else {}
        description_html = "\n".join(
            f"<h3>{s.get('title', '')}</h3>{s.get('text', '')}"
            for key in ("jobDescription", "qualifications", "additionalInformation")
            if (s := sections.get(key)) and s.get("text")
        )
        loc = item.get("location") or {}
        postings.append(
            RawPosting(
                source="smartrecruiters",
                source_job_id=str(item["id"]),
                title=(item.get("name") or "").strip(),
                apply_url=(detail or {}).get("postingUrl") or (detail or {}).get("applyUrl") or "",
                location_raw=loc.get("fullLocation")
                or join_nonempty(loc.get("city"), loc.get("region"), loc.get("country")),
                description_html=description_html or None,
                description_text=html_to_text(description_html),
                department=(item.get("department") or {}).get("label"),
                employment_type_raw=(item.get("typeOfEmployment") or {}).get("label"),
                workplace_type_raw="Remote" if loc.get("remote") else None,
                country_code=(loc.get("country") or "").upper() or None,
                posted_at=parse_datetime(item.get("releasedDate")),
            )
        )
    return postings
