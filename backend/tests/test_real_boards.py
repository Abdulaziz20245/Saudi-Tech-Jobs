"""Tests on real responses saved with `collector.discover --save-fixtures` (2026-10-20)."""

import respx

from collector.location import is_saudi
from collector.models import CompanyConfig
from collector.sources import greenhouse, workable
from tests.conftest import load_fixture


def fetch_saved(module, ats, ident, client):
    respx.get(module.URL.format(id=ident)).respond(json=load_fixture(f"{ats}/{ident}.json"))
    return module.fetch(client, CompanyConfig(name=ident, slug=ident, ats=ats, id=ident))


@respx.mock
def test_workable_merges_multi_city_listings(client):
    postings = fetch_saved(workable, "workable", "salla", client)

    # Salla lists 39 entries, but jobs open in several cities repeat once per city.
    assert len(postings) == 30
    assert len({p.source_job_id for p in postings}) == 30
    dpo = next(p for p in postings if p.source_job_id == "8AD90B7294")
    assert all(city in dpo.location_raw for city in ("Jeddah", "Makkah", "Al Khobar"))
    assert all(is_saudi(p) for p in postings)


@respx.mock
def test_workable_real_foodics_board(client):
    postings = fetch_saved(workable, "workable", "foodics", client)

    assert len(postings) == len({p.source_job_id for p in postings})
    assert all(p.title and p.apply_url.startswith("https://") for p in postings)
    assert all("<" not in p.description_text for p in postings)
    assert any(is_saudi(p) for p in postings)
    assert not all(is_saudi(p) for p in postings)


@respx.mock
def test_greenhouse_real_tamara_board(client):
    postings = fetch_saved(greenhouse, "greenhouse", "tamara", client)
    saudi = [p for p in postings if is_saudi(p)]

    assert len(postings) == 43
    assert len(saudi) == 15
    assert not any("Dubai" in p.location_raw and "Saudi" not in p.location_raw for p in saudi)
    assert all(p.description_text and "&lt;" not in p.description_text for p in postings)
    assert all(p.posted_at is not None for p in postings)
