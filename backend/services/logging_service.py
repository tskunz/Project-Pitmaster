"""Structured event logging for cook sessions."""

import logging
import json
from datetime import datetime

logger = logging.getLogger("pitmaster")


def log_event(
    event_type: str,
    session_id: str = "",
    **kwargs,
) -> None:
    """Log a structured event."""
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event_type,
        "session_id": session_id,
        **kwargs,
    }
    logger.info(json.dumps(entry))


def setup_logging() -> None:
    """Configure structured logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )
