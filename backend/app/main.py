"""FastAPI entry point. Dashboard endpoints arrive in Milestone 3."""

from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import get_settings
from db.models import Posting
from db.session import get_db

settings = get_settings()

app = FastAPI(title="Saudi Tech Jobs API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health(db: Annotated[Session, Depends(get_db)]) -> dict[str, object]:
    open_postings = db.scalar(
        select(func.count()).select_from(Posting).where(Posting.closed_at.is_(None))
    )
    return {"status": "ok", "open_postings": open_postings}
