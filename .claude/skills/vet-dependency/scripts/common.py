#!/usr/bin/env python3
"""Shared utilities for vet-dependency scripts.

Provides HTTP helpers, structured JSON output formatting, and error handling
used across all registry-specific vetting scripts (vet_pypi.py, vet_npm.py,
vet_gh_action.py).

All functions use only the Python standard library — no third-party
dependencies.
"""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

USER_AGENT = "omniwatcher-vet-dependency/0.1"
DEFAULT_TIMEOUT_SECONDS = 15
MAX_RETRIES = 2
RETRY_DELAY_SECONDS = 3


class VetError(Exception):
    """Raised when a vetting operation fails in a non-recoverable way.

    Args:
        message: Human-readable description of the failure.
        url: The URL that was being fetched when the error occurred, if any.
    """

    def __init__(self, message: str, url: str | None = None) -> None:
        super().__init__(message)
        self.url = url


@dataclass
class VetReport:
    """Structured output for a dependency vetting run.

    Attributes:
        package: The package name that was vetted.
        registry: The registry that was queried (e.g., "pypi", "npm", "gh-action").
        signals: Raw signals collected from the registry and security APIs.
        errors: Non-fatal errors encountered during vetting.
        timestamp: ISO 8601 timestamp of when the report was generated.
    """

    package: str
    registry: str
    signals: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_json(self) -> str:
        """Serialize the report to a JSON string.

        Returns:
            A pretty-printed JSON string suitable for stdout.
        """
        return json.dumps(asdict(self), indent=2)


def http_get_json(url: str, *, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> Any:
    """Fetch JSON from a URL with retries and error handling.

    Args:
        url: The URL to fetch.
        timeout: Request timeout in seconds.

    Returns:
        The parsed JSON response body.

    Raises:
        VetError: If the request fails after all retry attempts.
    """
    last_error: Exception | None = None

    for attempt in range(1, MAX_RETRIES + 2):
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "application/json",
                },
            )
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read().decode("utf-8")
                return json.loads(body)
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt <= MAX_RETRIES:
                time.sleep(RETRY_DELAY_SECONDS)

    raise VetError(
        f"Failed to fetch {url} after {MAX_RETRIES + 1} attempts: {last_error}",
        url=url,
    )


def http_get_text(url: str, *, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> str:
    """Fetch raw text from a URL with retries and error handling.

    Args:
        url: The URL to fetch.
        timeout: Request timeout in seconds.

    Returns:
        The response body as a string.

    Raises:
        VetError: If the request fails after all retry attempts.
    """
    last_error: Exception | None = None

    for attempt in range(1, MAX_RETRIES + 2):
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": USER_AGENT},
            )
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.read().decode("utf-8")
        except (urllib.error.URLError, urllib.error.HTTPError) as exc:
            last_error = exc
            if attempt <= MAX_RETRIES:
                time.sleep(RETRY_DELAY_SECONDS)

    raise VetError(
        f"Failed to fetch {url} after {MAX_RETRIES + 1} attempts: {last_error}",
        url=url,
    )


def emit_report(report: VetReport) -> None:
    """Print a VetReport as JSON to stdout and exit.

    Exits 0 if no errors were recorded, 1 if the report contains errors.

    Args:
        report: The completed vetting report.
    """
    print(report.to_json())
    sys.exit(1 if report.errors else 0)


def fail(package: str, registry: str, message: str) -> None:
    """Emit a minimal error report and exit with code 1.

    Use this for fatal errors that prevent any signals from being collected.

    Args:
        package: The package name that was being vetted.
        registry: The registry being queried.
        message: Human-readable error description.
    """
    report = VetReport(package=package, registry=registry, errors=[message])
    print(report.to_json(), file=sys.stderr)
    sys.exit(1)
