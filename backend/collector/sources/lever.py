"""Lever Postings API: https://github.com/lever/postings-api"""

from collector.http import PoliteClient, SourceError
from collector.models import CompanyConfig, RawPosting
from collector.sources._util import join_nonempty, parse_datetime
from collector.text import html_to_text

URL = "https://api.lever.co/v0/postings/{id}"


def fetch(client: PoliteClient, company: CompanyConfig) -> list[RawPosting]:
    data = client.get_json(URL.format(id=company.id), params={"mode": "json"})
    if not isinstance(data, list):
        raise SourceError(f"lever/{company.id}: unexpected response shape")

    postings = []
    for job in data:
        categories = job.get("categories") or {}
        all_locations = categories.get("allLocations") or []
        location = join_nonempty(categories.get("location"), *all_locations, sep=" | ")

        sections = [job.get("description") or ""]
        for item in job.get("lists") or []:
            sections.append(f"<h3>{item.get('text', '')}</h3><ul>{item.get('content', '')}</ul>")
        sections.append(job.get("additional") or "")
        description_html = "\n".join(s for s in sections if s)

        postings.append(
            RawPosting(
                source="lever",
                source_job_id=str(job["id"]),
                title=(job.get("text") or "").strip(),
                apply_url=job.get("hostedUrl") or job.get("applyUrl") or "",
                location_raw=location,
                description_html=description_html,
                description_text=html_to_text(description_html),
                department=categories.get("team") or categories.get("department"),
                employment_type_raw=categories.get("commitment"),
                workplace_type_raw=job.get("workplaceType"),
                country_code=job.get("country"),
                posted_at=parse_datetime(job.get("createdAt")),
            )
        )
    return postings
