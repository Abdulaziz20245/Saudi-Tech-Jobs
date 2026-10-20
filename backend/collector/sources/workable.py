"""Workable public widget API (powers embeddable careers pages)."""

from collector.http import PoliteClient, SourceError
from collector.models import CompanyConfig, RawPosting
from collector.sources._util import join_nonempty, parse_datetime
from collector.text import html_to_text

URL = "https://apply.workable.com/api/v1/widget/accounts/{id}"


def fetch(client: PoliteClient, company: CompanyConfig) -> list[RawPosting]:
    data = client.get_json(URL.format(id=company.id), params={"details": "true"})
    if not isinstance(data, dict) or not isinstance(data.get("jobs"), list):
        raise SourceError(f"workable/{company.id}: unexpected response shape")

    postings = []
    for job in data["jobs"]:
        locations = [
            join_nonempty(loc.get("city"), loc.get("region"), loc.get("country"))
            for loc in job.get("locations") or []
            if not loc.get("hidden")
        ]
        location = join_nonempty(
            join_nonempty(job.get("city"), job.get("state"), job.get("country")),
            *locations,
            sep=" | ",
        )
        country_codes = {loc.get("countryCode") for loc in job.get("locations") or []}
        description_html = job.get("description")
        postings.append(
            RawPosting(
                source="workable",
                source_job_id=str(job.get("shortcode") or job.get("code")),
                title=(job.get("title") or "").strip(),
                apply_url=job.get("url") or job.get("shortlink") or "",
                location_raw=location,
                description_html=description_html,
                description_text=html_to_text(description_html),
                department=job.get("department") or None,
                employment_type_raw=job.get("employment_type") or None,
                workplace_type_raw="Remote" if job.get("telecommuting") else None,
                country_code="SA" if "SA" in country_codes else None,
                posted_at=parse_datetime(job.get("published_on") or job.get("created_at")),
            )
        )
    return postings
