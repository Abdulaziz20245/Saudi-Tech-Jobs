"""Polite HTTP client: identifies itself, rate limits per host, retries transient errors."""

import time
from types import TracebackType
from typing import Any
from urllib.parse import urlparse

import httpx

RETRY_STATUSES = {429, 500, 502, 503, 504}


class SourceError(Exception):
    """A source could not be read (network error or unexpected response)."""


class PoliteClient:
    def __init__(
        self,
        user_agent: str,
        rate_limit_per_sec: float = 1.0,
        timeout: float = 30.0,
        max_attempts: int = 3,
        transport: httpx.BaseTransport | None = None,
        sleep: Any = time.sleep,
    ) -> None:
        self._client = httpx.Client(
            headers={"User-Agent": user_agent, "Accept": "application/json"},
            timeout=timeout,
            follow_redirects=True,
            transport=transport,
        )
        self._min_interval = 1.0 / rate_limit_per_sec if rate_limit_per_sec > 0 else 0.0
        self._last_request: dict[str, float] = {}
        self._max_attempts = max_attempts
        self._sleep = sleep

    def get_json(self, url: str, params: dict[str, Any] | None = None) -> Any:
        host = urlparse(url).netloc
        last_error: Exception | None = None
        for attempt in range(1, self._max_attempts + 1):
            self._wait_for(host)
            try:
                response = self._client.get(url, params=params)
            except httpx.TransportError as exc:
                last_error = exc
            else:
                if response.status_code == 200:
                    try:
                        return response.json()
                    except ValueError as exc:
                        raise SourceError(f"{url}: response is not JSON") from exc
                if response.status_code not in RETRY_STATUSES:
                    raise SourceError(f"{url}: HTTP {response.status_code}")
                last_error = SourceError(f"{url}: HTTP {response.status_code}")
            if attempt < self._max_attempts:
                self._sleep(2**attempt)
        raise SourceError(f"{url}: failed after {self._max_attempts} attempts: {last_error}")

    def _wait_for(self, host: str) -> None:
        now = time.monotonic()
        previous = self._last_request.get(host)
        if previous is not None:
            remaining = self._min_interval - (now - previous)
            if remaining > 0:
                self._sleep(remaining)
        self._last_request[host] = time.monotonic()

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "PoliteClient":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()
