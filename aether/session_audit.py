"""
SessionEvent audit bridge for Aether (Sprint A Phase 1 + Sprint C flywheel).

Soft-imports coastal_alpine_core.SessionEventStore when available.
Falls back to a Null store so Aether remains usable without Core installed.

Sprint C: optional record_session_trajectory on session_end / error
(outcome-level DataFlywheel sample; soft-import).

CAT stamp: local-first JSONL, no secrets in payloads, HITL evidence only.
Events never drive decisions — Guardrails + ThreatModeler remain authoritative.
"""

from __future__ import annotations

import logging
import time
import uuid
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("Aether.SessionAudit")

# ---------------------------------------------------------------------------
# Soft import of Core
# ---------------------------------------------------------------------------
try:
    from coastal_alpine_core import SessionEventStore, make_event  # type: ignore
    from coastal_alpine_core.session_events import EVENT_TYPES  # type: ignore

    HAS_CORE = True
except ImportError:  # pragma: no cover
    HAS_CORE = False
    EVENT_TYPES = frozenset()  # type: ignore

    def make_event(**kwargs: Any) -> Any:  # type: ignore
        return None

    class SessionEventStore:  # type: ignore
        """Placeholder so type checkers are happy when Core is absent."""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        def emit(self, **kwargs: Any) -> None:
            pass

        def append(self, event: Any) -> Any:
            return event


try:
    from coastal_alpine_core import record_session_trajectory  # type: ignore

    HAS_FLYWHEEL = True
except ImportError:  # pragma: no cover
    HAS_FLYWHEEL = False

    def record_session_trajectory(**kwargs: Any) -> None:  # type: ignore
        return None


class NullSessionEventStore:
    """No-op store used when coastal-alpine-core is not installed."""

    def emit(self, **kwargs: Any) -> None:
        return None

    def append(self, event: Any) -> Any:
        return event

    def list_session(self, *args: Any, **kwargs: Any) -> list:
        return []

    def resume_from(self, *args: Any, **kwargs: Any) -> list:
        return []


def default_event_path() -> Path:
    return Path.home() / ".aether" / "session_events.jsonl"


def default_flywheel_path() -> Path:
    return Path.home() / ".aether" / "flywheel_trajectories.jsonl"


def get_store(
    storage_path: Optional[str | Path] = None,
    force_null: bool = False,
) -> Any:
    """Return a real SessionEventStore when Core is present, else Null."""
    if force_null or not HAS_CORE:
        return NullSessionEventStore()
    path = Path(storage_path) if storage_path else default_event_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    return SessionEventStore(str(path))


def install_session_event_hooks(
    orch: Any,
    store: Optional[Any] = None,
    tenant_id: Optional[str] = None,
    storage_path: Optional[str | Path] = None,
    flywheel_path: Optional[str | Path] = None,
) -> None:
    """
    Install thin SessionEvent wrappers on an AetherOrchestrator instance.

    Idempotent: calling twice is safe (re-uses existing _event_store).
    Does not alter control flow or HITL decisions.
    Sprint C: also records outcome Trajectories when Core ≥0.5.9 is present.
    """
    if getattr(orch, "_session_hooks_installed", False):
        return

    event_store = store if store is not None else get_store(storage_path)
    orch._event_store = event_store
    orch._event_tenant_id = tenant_id
    orch._session_id: Optional[str] = None
    orch._flywheel_path = str(flywheel_path or default_flywheel_path())
    orch._session_t0: Optional[float] = None

    def _emit(event_type: str, actor: str, payload: Optional[dict] = None, **extra: Any) -> None:
        sid = getattr(orch, "_session_id", None)
        if not sid:
            return
        try:
            event_store.emit(
                session_id=sid,
                event_type=event_type,
                actor=actor,
                tenant_id=getattr(orch, "_event_tenant_id", None),
                payload=payload or {},
                **extra,
            )
        except Exception as exc:
            logger.debug("SessionEvent emit failed (%s): %s", event_type, exc)

    def _record_traj(outcome: str, method: str, payload: Optional[dict] = None) -> None:
        if not HAS_FLYWHEEL:
            return
        sid = getattr(orch, "_session_id", None)
        if not sid:
            return
        t0 = getattr(orch, "_session_t0", None) or time.perf_counter()
        try:
            record_session_trajectory(
                session_id=sid,
                action=f"aether.{method}",
                outcome=outcome,
                input_summary=f"method={method}",
                output_summary=str(payload or {})[:200],
                latency_seconds=max(0.0, time.perf_counter() - t0),
                tenant_id=getattr(orch, "_event_tenant_id", None),
                storage_path=getattr(orch, "_flywheel_path", None),
            )
        except Exception as exc:
            logger.debug("Trajectory record failed: %s", exc)

    original_start = orch.start_task

    def start_task(goal: str):
        orch._session_id = str(uuid.uuid4())
        orch._session_t0 = time.perf_counter()
        state = original_start(goal)
        _emit(
            "session_start",
            actor="orchestrator",
            payload={"goal_chars": len(goal or "")},
        )
        _emit(
            "prompt_received",
            actor="orchestrator",
            payload={"chars": len(goal or ""), "source": "goal"},
        )
        return state

    orch.start_task = start_task  # type: ignore[method-assign]

    original_call_tool = orch.call_tool

    def call_tool(tool_name: str, **kwargs):
        _emit(
            "tool_call",
            actor="orchestrator",
            payload={"tool": tool_name, "arg_keys": sorted(kwargs.keys())},
        )
        result = original_call_tool(tool_name, **kwargs)
        _emit(
            "tool_result",
            actor="orchestrator",
            payload={
                "tool": tool_name,
                "success": bool(getattr(result, "success", False)),
                "cached": bool((getattr(result, "metadata", None) or {}).get("cached", False)),
            },
            outcome="success" if getattr(result, "success", False) else "error",
        )
        return result

    orch.call_tool = call_tool  # type: ignore[method-assign]

    original_execute_skill = orch._execute_skill

    def _execute_skill(skill_name: str, goal: str):
        result = original_execute_skill(skill_name, goal)
        _emit(
            "skill_applied",
            actor="orchestrator",
            payload={
                "skill": skill_name,
                "applied": bool(result.get("applied")),
                "requires_hitl": bool(result.get("requires_hitl")),
                "cultural_sensitivity": result.get("cultural_sensitivity", "low"),
            },
            outcome="applied" if result.get("applied") else "failed",
        )
        return result

    orch._execute_skill = _execute_skill  # type: ignore[method-assign]

    original_approve = orch._approve_if_needed

    def _approve_if_needed(action: str, context: str = "") -> bool:
        needs = False
        try:
            needs = orch._requires_approval(action, context=context) or getattr(
                orch, "_goal_injection_locked", False
            )
        except Exception:
            needs = True

        if needs:
            _emit(
                "approval_required",
                actor="orchestrator",
                payload={"action": action},
            )

        approved = original_approve(action, context=context)

        if needs:
            _emit(
                "approval_granted" if approved else "approval_denied",
                actor="human" if approved else "orchestrator",
                payload={"action": action},
                outcome="granted" if approved else "denied",
            )
        return approved

    orch._approve_if_needed = _approve_if_needed  # type: ignore[method-assign]

    for method_name in ("run_react_loop", "run_pipeline"):
        original = getattr(orch, method_name, None)
        if original is None:
            continue

        def _make_wrapper(orig, name: str):
            def wrapper(goal: str, *args, **kwargs):
                try:
                    state = orig(goal, *args, **kwargs)
                    payload = {
                        "method": name,
                        "phase": getattr(state, "current_phase", None),
                        "tool_calls": len(getattr(state, "tool_calls", []) or []),
                        "errors": len(getattr(orch, "errors", []) or []),
                    }
                    _emit("session_end", actor="orchestrator", payload=payload)
                    _record_traj("success", name, payload)
                    return state
                except Exception as exc:
                    _emit(
                        "error",
                        actor="orchestrator",
                        payload={"method": name, "error_type": type(exc).__name__},
                        outcome="error",
                    )
                    _record_traj("error", name, {"error_type": type(exc).__name__})
                    raise

            return wrapper

        setattr(orch, method_name, _make_wrapper(original, method_name))

    orch._session_hooks_installed = True
    logger.info(
        "SessionEvent hooks installed (Core=%s, flywheel=%s, tenant=%s)",
        HAS_CORE,
        HAS_FLYWHEEL,
        tenant_id,
    )
