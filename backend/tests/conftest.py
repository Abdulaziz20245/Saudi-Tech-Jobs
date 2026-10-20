import json
import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from collector.http import PoliteClient
from db.models import Base

FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(relative: str) -> Any:
    return json.loads((FIXTURES / relative).read_text(encoding="utf-8"))


@pytest.fixture
def client() -> Iterator[PoliteClient]:
    """HTTP client with sleeping disabled; pair with respx to mock responses."""
    with PoliteClient("test-agent", rate_limit_per_sec=1000, sleep=lambda _s: None) as c:
        yield c


@pytest.fixture
def session() -> Iterator[Session]:
    """Fresh database per test. Uses TEST_DATABASE_URL (Postgres in CI) or in-memory SQLite."""
    url = os.environ.get("TEST_DATABASE_URL", "sqlite+pysqlite:///:memory:")
    if url.startswith("sqlite"):
        # One shared connection so FastAPI's worker thread sees the same in-memory database.
        engine = create_engine(url, connect_args={"check_same_thread": False}, poolclass=StaticPool)
    else:
        engine = create_engine(url)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with Session(engine) as s:
        yield s
    Base.metadata.drop_all(engine)
    engine.dispose()
