"""Load the curated company list from data/companies.yaml."""

import re
from pathlib import Path
from typing import get_args

import yaml

from collector.models import AtsType, CompanyConfig

SUPPORTED_ATS: tuple[str, ...] = get_args(AtsType)


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def load_companies(path: Path, include_unverified: bool = True) -> list[CompanyConfig]:
    """Return companies with a supported ATS and identifier; skip the rest."""
    entries = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    companies = []
    for entry in entries:
        ats, ident = entry.get("ats"), entry.get("id")
        if ats not in SUPPORTED_ATS or not ident:
            continue
        if not include_unverified and not entry.get("verified"):
            continue
        companies.append(
            CompanyConfig(
                name=entry["name"],
                slug=slugify(entry["name"]),
                ats=ats,
                id=str(ident),
                website=entry.get("website"),
            )
        )
    return companies
