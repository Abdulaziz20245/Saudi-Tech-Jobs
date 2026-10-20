from datetime import UTC, datetime
from typing import Any


def parse_datetime(value: Any) -> datetime | None:
    """Parse ISO 8601 strings, YYYY-MM-DD dates, or epoch milliseconds into aware datetimes."""
    if value is None or value == "":
        return None
    if isinstance(value, int | float):
        return datetime.fromtimestamp(value / 1000, tz=UTC)
    if isinstance(value, str):
        text = value.strip().replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            return None
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
    return None


def join_nonempty(*parts: Any, sep: str = ", ") -> str:
    return sep.join(str(p).strip() for p in parts if p and str(p).strip())
