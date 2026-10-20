"""One adapter per job-board system. Each exposes `fetch(client, company) -> list[RawPosting]`.

Endpoints and response shapes are documented in docs/DATA_SOURCES.md. Adapters read fields
defensively (`.get`) because vendors add and omit fields between companies.
"""

from collections.abc import Callable

from collector.http import PoliteClient
from collector.models import AtsType, CompanyConfig, RawPosting
from collector.sources import ashby, greenhouse, lever, smartrecruiters, workable

Fetcher = Callable[[PoliteClient, CompanyConfig], list[RawPosting]]

ADAPTERS: dict[AtsType, Fetcher] = {
    "greenhouse": greenhouse.fetch,
    "lever": lever.fetch,
    "ashby": ashby.fetch,
    "workable": workable.fetch,
    "smartrecruiters": smartrecruiters.fetch,
}
