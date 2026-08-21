# Copyright (c) 2026 Coastal Alpine Tech Limited. All rights reserved.
"""
Aether Code Mode / PTC bridge (Sprint E).

Soft-imports Core CodeModeRunner when coastal-alpine-core ≥0.5.10 is present.
Falls back to a clear error result when Core is unavailable.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Dict, Mapping, Optional

logger = logging.getLogger("aether.code_mode")

try:
    from coastal_alpine_core import CodeModeResult, CodeModeRunner
except ImportError:  # pragma: no cover
    CodeModeRunner = None  # type: ignore
    CodeModeResult = None  # type: ignore


def run_code_mode(
    source: str,
    tools: Mapping[str, Callable[..., Any]],
    *,
    hitl: Optional[Callable[[str], bool]] = None,
    max_chars: int = 4000,
) -> Dict[str, Any]:
    """Execute restricted agent code against a tool map. Returns a plain dict."""
    if CodeModeRunner is None:
        return {
            "success": False,
            "error": "code_mode_requires_core_0.5.10",
            "output": None,
            "tool_calls": [],
        }

    runner = CodeModeRunner(tools, hitl=hitl, max_chars=max_chars)
    result = runner.run(source)
    return {
        "success": bool(result.success),
        "output": result.output,
        "error": result.error,
        "tool_calls": list(result.tool_calls or []),
    }
