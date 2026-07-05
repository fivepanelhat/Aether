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
Codebase Search Tool
"""

from .base import Tool, ToolResult
from typing import Optional
import os
import fnmatch


class CodebaseSearchTool(Tool):
    name = "codebase_search"
    description = "Search for a string across files in a directory."
    input_schema = {
        "query": "String to search for",
        "directory": "Directory to search in",
        "file_pattern": "Optional glob pattern (e.g. *.py)",
        "max_results": "Maximum results to return"
    }

    def run(
        self,
        query: str,
        directory: str = ".",
        file_pattern: Optional[str] = None,
        max_results: int = 20
    ) -> ToolResult:
        try:
            matches = []
            for root, dirs, files in os.walk(directory):
                dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "node_modules"}]
                for filename in files:
                    if file_pattern and not fnmatch.fnmatch(filename, file_pattern):
                        continue
                    filepath = os.path.join(root, filename)
                    try:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            for line_num, line in enumerate(f, 1):
                                if query.lower() in line.lower():
                                    matches.append({
                                        "file": filepath,
                                        "line": line_num,
                                        "content": line.strip()
                                    })
                                    if len(matches) >= max_results:
                                        break
                    except Exception:
                        continue
                    if len(matches) >= max_results:
                        break
                if len(matches) >= max_results:
                    break

            return ToolResult(success=True, output=matches)
        except Exception as e:
            return ToolResult(success=False, error=str(e))
