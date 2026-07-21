# Copyright (c) 2026 Coastal Alpine Tech Limited. All rights reserved.
# Proprietary and confidential. No open-source grant is implied by access to
# this file; use is governed solely by the LICENSE at the repository root.
"""
Tool Executor with Caching Support
"""

from .base import ToolResult
from .cache import ToolCache
from typing import Optional


class ToolExecutor:
    def __init__(self, registry, cache: Optional[ToolCache] = None):
        self.registry = registry
        self.cache = cache or ToolCache()

        # Tools that should be cached (add more as needed)
        self.cacheable_tools = {"codebase_search", "memory_query"}

    def execute(self, tool_name: str, **kwargs) -> ToolResult:
        tool = self.registry.get(tool_name)

        if not tool:
            return ToolResult(
                success=False,
                error=f"Tool '{tool_name}' not found."
            )

        # Check cache first for cacheable tools
        if tool_name in self.cacheable_tools:
            cached_result = self.cache.get(tool_name, **kwargs)
            if cached_result is not None:
                return ToolResult(
                    success=True,
                    output=cached_result,
                    metadata={"cached": True}
                )

        try:
            result = tool.run(**kwargs)

            # Cache successful results for cacheable tools
            if tool_name in self.cacheable_tools and result.success:
                self.cache.set(tool_name, result.output, **kwargs)

            return result

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error executing tool '{tool_name}': {str(e)}"
            )
