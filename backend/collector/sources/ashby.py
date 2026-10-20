"""Ashby Job Posting API: https://developers.ashbyhq.com/reference/jobpostingapi"""

from collector.http import PoliteClient, SourceError
from collector.models import CompanyConfig, RawPosting
from collector.sources._util import join_nonempty, parse_datetime
from collector.text import html_to_text

URL = "https://api.ashbyhq.com/posting-api/job-board/{id}"


def fetch(client: PoliteClient, company: CompanyConfig) -> list[RawPosting]:
    data = client.get_json(URL.format(id=company.id), params={"includeCompensation": "true"})
    if not isinstance(data, dict) or not isinstance(data.get("jobs"), list):
        raise SourceError(f"ashby/{company.id}: unexpected response shape")

    postings = []
    for job in data["jobs"]:
        if job.get("isListed") is False:
            continue
        secondary = [s.get("location") for s in job.get("secondaryLocations") or []]
        address = (job.get("address") or {}).get("postalAddress") or {}
        location = join_nonempty(
            job.get("location"),
            *secondary,
            address.get("addressLocality"),
            address.get("addressCountry"),
            sep=" | ",
        )
        description_html = job.get("descriptionHtml")
        workplace = job.get("workplaceType") or ("Remote" if job.get("isRemote") else None)
        postings.append(
            RawPosting(
                source="ashby",
                source_job_id=str(job["id"]),
                title=(job.get("title") or "").strip(),
                apply_url=job.get("jobUrl") or job.get("applyUrl") or "",
                location_raw=location,
                description_html=description_html,
                description_text=job.get("descriptionPlain") or html_to_text(description_html),
                department=job.get("department") or job.get("team"),
                employment_type_raw=job.get("employmentType"),
                workplace_type_raw=workplace,
                posted_at=parse_datetime(job.get("publishedAt")),
            )
        )
    return postings
