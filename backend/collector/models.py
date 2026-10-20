from dataclasses import dataclass
from datetime import datetime
from typing import Literal

AtsType = Literal["greenhouse", "lever", "ashby", "workable", "smartrecruiters"]


@dataclass(frozen=True)
class CompanyConfig:
    """One entry of data/companies.yaml."""

    name: str
    slug: str
    ats: AtsType
    id: str
    website: str | None = None


@dataclass
class RawPosting:
    """A posting as returned by a source, normalized to a common shape."""

    source: AtsType
    source_job_id: str
    title: str
    apply_url: str
    location_raw: str = ""
    description_html: str | None = None
    description_text: str = ""
    department: str | None = None
    employment_type_raw: str | None = None
    workplace_type_raw: str | None = None
    country_code: str | None = None  # ISO 3166-1 alpha-2 when the source provides it
    posted_at: datetime | None = None
