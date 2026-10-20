"""Greenhouse Job Board API: https://developers.greenhouse.io/job-board.html"""

from collector.http import PoliteClient, SourceError
from collector.models import CompanyConfig, RawPosting
from collector.sources._util import join_nonempty, parse_datetime
from collector.text import html_to_text

URL = "https://boards-api.greenhouse.io/v1/boards/{id}/jobs"


def fetch(client: PoliteClient, company: CompanyConfig) -> list[RawPosting]:
    data = client.get_json(URL.format(id=company.id), params={"content": "true"})
    if not isinstance(data, dict) or not isinstance(data.get("jobs"), list):
        raise SourceError(f"greenhouse/{company.id}: unexpected response shape")

    postings = []
    for job in data["jobs"]:
        offices = job.get("offices") or []
        office_locations = [o.get("location") or o.get("name") for o in offices]
        location = join_nonempty(
            (job.get("location") or {}).get("name"), *office_locations, sep=" | "
        )
        departments = job.get("departments") or []
        description_html = job.get("content")
        postings.append(
            RawPosting(
                source="greenhouse",
                source_job_id=str(job["id"]),
                title=(job.get("title") or "").strip(),
                apply_url=job.get("absolute_url") or "",
                location_raw=location,
                description_html=description_html,
                description_text=html_to_text(description_html),
                department=departments[0].get("name") if departments else None,
                posted_at=parse_datetime(job.get("first_published") or job.get("updated_at")),
            )
        )
    return postings
