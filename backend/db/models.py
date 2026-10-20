"""Database models. See docs/ARCHITECTURE.md for the full data model.

Extraction tables (posting_extractions, skills, posting_skills) arrive in Milestone 2.
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    slug: Mapped[str] = mapped_column(String(200), unique=True)
    website: Mapped[str | None] = mapped_column(String(500))
    ats_type: Mapped[str] = mapped_column(String(40))
    ats_identifier: Mapped[str] = mapped_column(String(200))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_collected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_error: Mapped[str | None] = mapped_column(Text)

    postings: Mapped[list["Posting"]] = relationship(back_populates="company")


class Posting(Base):
    __tablename__ = "postings"
    __table_args__ = (UniqueConstraint("source", "source_job_id", name="uq_posting_source"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), index=True)
    source: Mapped[str] = mapped_column(String(40))
    source_job_id: Mapped[str] = mapped_column(String(200))

    title: Mapped[str] = mapped_column(String(500))
    description_html: Mapped[str | None] = mapped_column(Text)
    description_text: Mapped[str] = mapped_column(Text, default="")
    language: Mapped[str] = mapped_column(String(10))  # en | ar | mixed
    location_raw: Mapped[str] = mapped_column(String(500), default="")
    department: Mapped[str | None] = mapped_column(String(200))
    employment_type_raw: Mapped[str | None] = mapped_column(String(100))
    workplace_type_raw: Mapped[str | None] = mapped_column(String(100))
    apply_url: Mapped[str] = mapped_column(String(1000))
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    content_hash: Mapped[str] = mapped_column(String(64))

    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)

    company: Mapped[Company] = relationship(back_populates="postings")


class CollectionRun(Base):
    """One collector pass, kept for monitoring and the 'last updated' label."""

    __tablename__ = "collection_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    companies_ok: Mapped[int] = mapped_column(Integer, default=0)
    companies_failed: Mapped[int] = mapped_column(Integer, default=0)
    postings_new: Mapped[int] = mapped_column(Integer, default=0)
    postings_updated: Mapped[int] = mapped_column(Integer, default=0)
    postings_closed: Mapped[int] = mapped_column(Integer, default=0)
