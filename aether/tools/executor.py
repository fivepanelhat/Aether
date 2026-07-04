"""
Tool Executor
Handles safe execution of tools with error handling.
"""

from .base import Tool, ToolResult
from typing import Any


class ToolExecutor:
    def __init__(self, registry):
        self.registry = registry

    def execute(self, tool_name: str, **kwargs) -> ToolResult:
        """Execute a tool by name."""
        tool = self.registry.get(tool_name)

        if not tool:
            return ToolResult(
                success=False,
                error=f"Tool '{tool_name}' not found in registry."
            )

        try:
            result = tool.run(**kwargs)
            return result
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error executing tool '{tool_name}': {str(e)}"
            )
