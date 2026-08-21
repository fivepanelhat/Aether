"""SessionEvent audit bridge for Aether (Sprint A Phase 1).

Soft-imports coastal_alpine_core.SessionEventStore so Aether remains runnable
without Core installed. When Core is present, emits the shared CAT event
vocabulary for HITL / Trajectory evidence.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any, Optional

logger = logging.getLogger("Aether.SessionAudit")

try:
    from coastal_alpine_core.session_events import SessionEventStore as _Store
    _HAS_CORE = True
except ImportError:  # pragma: no cover - optional dependency
    _Store = None  # type: ignore
    _HAS_CORE = False


class NullSessionEventStore:
    """No-op stand-in when coastal-alpine-core is not installed."""

    def emit(self, **kwargs: Any) -> None:
        return None

    def list_session(self, *args: Any, **kwargs: Any) -> list:
        return []


def make_session_store(
    storage_path: str = "aether_session_events.jsonl",
    event_store: Any = None,
) -> Any:
    if event_store is not None:
        return event_store
    if _HAS_CORE and _Store is not None:
        return _Store(storage_path=storage_path)
    logger.debug("coastal-alpine-core not installed; SessionEvent audit disabled")
    return NullSessionEventStore()


def new_session_id() -> str:
    return str(uuid.uuid4())
