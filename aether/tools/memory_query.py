"""
Memory Query Tool
"""

from .base import Tool, ToolResult
from typing import Optional


class MemoryQueryTool(Tool):
    name = "memory_query"
    description = "Query the Aether memory system for past tasks and decisions."
    input_schema = {
        "query": "What to search for in memory",
        "limit": "Maximum number of results"
    }

    def __init__(self, memory_instance=None):
        super().__init__()
        self.memory = memory_instance

    def run(self, query: str, limit: int = 5) -> ToolResult:
        if not self.memory:
            return ToolResult(success=False, error="Memory system not connected.")

        try:
            hits = self.memory.search(query, limit=limit)
            results = [
                {
                    "timestamp": entry.timestamp,
                    "type": entry.type,
                    "content": entry.content,
                    "metadata": entry.metadata
                }
                for entry in hits
            ]

            return ToolResult(success=True, output=results)
        except Exception as e:
            return ToolResult(success=False, error=str(e))
