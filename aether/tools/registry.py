# Copyright (c) 2026 Coastal Alpine Tech Limited. All rights reserved.
# Proprietary and confidential. No open-source grant is implied by access to
# this file; use is governed solely by the LICENSE at the repository root.
"""
Tool Registry
Central place to register, discover, and retrieve tools.
"""

import logging
from typing import Dict, List, Optional
from .base import Tool

logger = logging.getLogger("AetherToolRegistry")


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        """Register a new tool."""
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered.")
        self._tools[tool.name] = tool
        logger.debug("Registered tool: %s", tool.name)

    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> List[Tool]:
        """Return all registered tools."""
        return list(self._tools.values())

    def list_tool_names(self) -> List[str]:
        """Return names of all registered tools."""
        return list(self._tools.keys())

    def get_tool_descriptions(self) -> str:
        """Return formatted descriptions of all tools (useful for prompts)."""
        if not self._tools:
            return "No tools registered."

        return "\n".join(
            f"- {tool.name}: {tool.description}"
            for tool in self._tools.values()
        )
