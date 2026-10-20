import respx
from sqlalchemy import select

from collector.companies import load_companies
from collector.models import CompanyConfig
from collector.run import collect
from collector.sources import greenhouse, workable
from db.models import Company, Posting
from tests.conftest import load_fixture


@respx.mock
def test_collect_keeps_going_when_one_board_fails(session, client):
    respx.get(workable.URL.format(id="good")).respond(
        json=load_fixture("workable/synthetic_board.json")
    )
    respx.get(greenhouse.URL.format(id="broken")).respond(status_code=404)
    companies = [
        CompanyConfig(name="Broken", slug="broken", ats="greenhouse", id="broken"),
        CompanyConfig(name="Good", slug="good", ats="workable", id="good"),
    ]

    run = collect(session, client, companies)

    assert (run.companies_ok, run.companies_failed, run.postings_new) == (1, 1, 1)
    titles = session.scalars(select(Posting.title)).all()
    assert titles == ["مهندس برمجيات - واجهات خلفية"]  # the Cairo role is filtered out
    broken = session.scalar(select(Company).where(Company.slug == "broken"))
    assert "404" in broken.last_error


def test_load_companies_skips_unknown_ats(tmp_path):
    path = tmp_path / "companies.yaml"
    path.write_text(
        "- {name: Foodics, ats: workable, id: foodics, verified: true}\n"
        "- {name: Tabby, ats: unknown, id: null}\n"
        "- {name: Lean Technologies, ats: lever, id: lean, verified: false}\n",
        encoding="utf-8",
    )
    assert [c.slug for c in load_companies(path)] == ["foodics", "lean-technologies"]
    assert [c.slug for c in load_companies(path, include_unverified=False)] == ["foodics"]
