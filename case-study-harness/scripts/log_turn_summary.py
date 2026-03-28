#!/usr/bin/env python3
"""Log per-turn summaries captured by the Stop hook.

Reads hook JSON from stdin and appends a turn_summary entry to
data/turn-summaries.jsonl. The Stop hook fires after each Claude
response (turn), not at session end.
"""

import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DATA_DIR: Path = Path(__file__).resolve().parent.parent / "data"
LOG_FILE: str = "turn-summaries.jsonl"

MAX_LENGTH: int = 2000


def truncate(text: str, max_length: int = MAX_LENGTH) -> str:
    """Truncate text to a maximum length with an ellipsis suffix.

    Args:
        text: The string to truncate.
        max_length: Maximum allowed length.

    Returns:
        The original string if within limits, or a truncated version with "...".
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def build_entry(
    session_id: str, description: str, stop_hook_active: bool
) -> dict[str, Any]:
    """Construct a turn_summary JSONL entry.

    Args:
        session_id: The session this turn belongs to.
        description: High-level summary of what Claude responded.
        stop_hook_active: Whether the stop hook is active (mid-turn vs. complete).

    Returns:
        A dictionary ready for JSON serialization.
    """
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "event_type": "turn_summary",
        "source": "hook",
        "session_id": session_id,
        "description": description,
        "stop_hook_active": stop_hook_active,
    }


def main() -> None:
    """Read Stop hook JSON from stdin and log a turn summary."""
    try:
        payload: dict[str, Any] = json.loads(sys.stdin.read())

        session_id: str = payload.get("session_id", "")
        last_message: str = payload.get("last_assistant_message", "")
        stop_hook_active: bool = payload.get("stop_hook_active", False)
        description = truncate(last_message)
        entry = build_entry(session_id, description, stop_hook_active)

        os.makedirs(DATA_DIR, exist_ok=True)
        with open(DATA_DIR / LOG_FILE, "a") as file:
            file.write(json.dumps(entry, default=str) + "\n")

    except (OSError, TypeError, ValueError):
        pass


if __name__ == "__main__":
    main()
