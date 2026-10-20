import httpx
import pytest
import respx

from collector.http import SourceError
from collector.location import is_saudi
from collector.models import CompanyConfig
from collector.sources import ashby, greenhouse, lever, smartrecruiters, workable
from tests.conftest import load_fixture


def company(ats, ident="example"):
    return CompanyConfig(name="Example", slug="example", ats=ats, id=ident)


@respx.mock
def test_greenhouse_parses_and_unescapes_content(client):
    respx.get(greenhouse.URL.format(id="example")).respond(
        json=load_fixture("greenhouse/synthetic_board.json")
    )
    postings = greenhouse.fetch(client, company("greenhouse"))

    assert len(postings) == 2
    job = postings[0]
    assert job.source_job_id == "4012345"
    assert job.title == "Senior Data Engineer"
    assert "Riyadh, Saudi Arabia" in job.location_raw
    assert job.department == "Data"
    assert "- Python" in job.description_text and "<" not in job.description_text
    assert job.posted_at is not None
    assert [is_saudi(p) for p in postings] == [True, False]


@respx.mock
def test_lever_includes_lists_and_country(client):
    respx.get(lever.URL.format(id="example")).respond(
        json=load_fixture("lever/synthetic_board.json")
    )
    postings = lever.fetch(client, company("lever"))

    job = postings[0]
    assert job.title == "Backend Engineer (Go)"
    assert job.country_code == "SA"
    assert job.workplace_type_raw == "hybrid"
    assert job.employment_type_raw == "Full-time"
    assert "Requirements" in job.description_text and "- PostgreSQL" in job.description_text
    assert job.apply_url.startswith("https://jobs.lever.co/")
    assert [is_saudi(p) for p in postings] == [True, False]


@respx.mock
def test_ashby_skips_unlisted_jobs(client):
    respx.get(ashby.URL.format(id="example")).respond(
        json=load_fixture("ashby/synthetic_board.json")
    )
    postings = ashby.fetch(client, company("ashby"))

    assert len(postings) == 1
    job = postings[0]
    assert job.title == "Machine Learning Engineer"
    assert "Jeddah" in job.location_raw
    assert job.description_text == "Train and ship LLM features."
    assert is_saudi(job)


@respx.mock
def test_workable_handles_arabic_and_country_code(client):
    respx.get(workable.URL.format(id="example")).respond(
        json=load_fixture("workable/synthetic_board.json")
    )
    postings = workable.fetch(client, company("workable"))

    arabic, remote = postings
    assert arabic.source_job_id == "ABC123DEF4"
    assert arabic.country_code == "SA"
    assert "Node.js" in arabic.description_text
    assert remote.workplace_type_raw == "Remote"
    assert [is_saudi(p) for p in postings] == [True, False]


@respx.mock
def test_smartrecruiters_fetches_details(client):
    base = "https://api.smartrecruiters.com/v1/companies/example/postings"
    respx.get(base).respond(json=load_fixture("smartrecruiters/synthetic_list.json"))
    respx.get(f"{base}/744000012345678").respond(
        json=load_fixture("smartrecruiters/synthetic_detail.json")
    )
    postings = smartrecruiters.fetch(client, company("smartrecruiters"))

    job = postings[0]
    assert job.country_code == "SA"
    assert "AWS and Azure" in job.description_text
    assert "About us" not in job.description_text
    assert job.apply_url.endswith("cloud-security-engineer")


@respx.mock
def test_not_found_raises_source_error(client):
    respx.get(greenhouse.URL.format(id="missing")).respond(status_code=404)
    with pytest.raises(SourceError, match="HTTP 404"):
        greenhouse.fetch(client, company("greenhouse", "missing"))


@respx.mock
def test_transient_errors_are_retried(client):
    route = respx.get(greenhouse.URL.format(id="example"))
    route.side_effect = [
        httpx.Response(503),
        httpx.ConnectError("boom"),
        httpx.Response(200, json={"jobs": []}),
    ]
    assert greenhouse.fetch(client, company("greenhouse")) == []
    assert route.call_count == 3


@respx.mock
def test_unexpected_shape_raises(client):
    respx.get(greenhouse.URL.format(id="example")).respond(json={"error": "nope"})
    with pytest.raises(SourceError, match="unexpected response shape"):
        greenhouse.fetch(client, company("greenhouse"))
