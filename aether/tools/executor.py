# Copyright 2026 Aether Project Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
