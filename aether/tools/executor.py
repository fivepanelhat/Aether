# Copyright (c) 2026 Coastal Alpine Tech Limited. All rights reserved.
# Proprietary and confidential. No open-source grant is implied by access to
# this file; use is governed solely by the LICENSE at the repository root.
"""
Tool Executor with Caching + optional reversible EffectJournal (Sprint E)
"""

from __future__ import annotations

from typing import Any, Optional

from .base import ToolResult
from .cache import ToolCache

try:
    from coastal_alpine_core import EffectJournal  # Core ≥0.5.10
except ImportError:  # pragma: no cover
    EffectJournal = None  # type: ignore


class ToolExecutor:
    def __init__(self, registry, cache: Optional[ToolCache] = None, journal: Any = None):
        self.registry = registry
        self.cache = cache or ToolCache()
        self.journal = journal
        if self.journal is None and EffectJournal is not None:
            try:
                self.journal = EffectJournal()
            except Exception:
                self.journal = None

        # Tools that should be cached (add more as needed)
        self.cacheable_tools = {"codebase_search", "memory_query"}

    def execute(self, tool_name: str, **kwargs) -> ToolResult:
        tool = self.registry.get(tool_name)

        if not tool:
            return ToolResult(
                success=False,
                error=f"Tool '{tool_name}' not found.",
            )

        if tool_name in self.cacheable_tools:
            cached_result = self.cache.get(tool_name, **kwargs)
            if cached_result is not None:
                return ToolResult(
                    success=True,
                    output=cached_result,
                    metadata={"cached": True},
                )

        try:
            result = tool.run(**kwargs)

            if tool_name in self.cacheable_tools and result.success:
                self.cache.set(tool_name, result.output, **kwargs)

            if self.journal is not None and result.success:
                try:
                    reversible = bool(
                        getattr(tool, "reversible", False)
                        or (result.metadata or {}).get("reversible")
                    )
                    reverse_action = (result.metadata or {}).get("reverse_action")
                    reverse_payload = (result.metadata or {}).get("reverse_payload") or {}
                    self.journal.record(
                        tool_name,
                        payload={"kwargs_keys": sorted(kwargs.keys())},
                        reverse_action=reverse_action,
                        reverse_payload=reverse_payload,
                        reversible=reversible,
                        metadata={"tool": tool_name},
                    )
                except Exception:
                    pass

            return result

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error executing tool '{tool_name}': {str(e)}",
            )

    def undo_last(self):
        if self.journal is None:
            return None
        return self.journal.undo_last()
