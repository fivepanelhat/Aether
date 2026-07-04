"""
Tool Registry
Central place to register, discover, and retrieve tools.
"""

from typing import Dict, List, Optional
from .base import Tool


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        """Register a new tool."""
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' is already registered.")
        self._tools[tool.name] = tool
        print(f"[ToolRegistry] Registered tool: {tool.name}")

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
