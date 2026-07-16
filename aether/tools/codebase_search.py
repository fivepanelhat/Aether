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
Codebase Search Tool (path-sandboxed)
"""

from .base import Tool, ToolResult
from typing import Optional
import os
import fnmatch

from aether.paths import is_within_allowed_root


class CodebaseSearchTool(Tool):
    name = "codebase_search"
    description = "Search for a string across files inside the allowed root."
    input_schema = {
        "query": "String to search for",
        "directory": "Directory to search in (must be inside allowed root)",
        "file_pattern": "Optional glob pattern (e.g. *.py)",
        "max_results": "Maximum results to return",
    }

    # Skip heavy / binary-ish extensions to keep search fast and useful
    _SKIP_EXT = {
        ".pyc", ".pyo", ".so", ".dll", ".exe", ".bin", ".o", ".a",
        ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf",
        ".zip", ".gz", ".tar", ".whl", ".egg",
    }
    _MAX_FILE_BYTES = 1_000_000

    def __init__(self, allowed_root: str = None):
        self.allowed_root = os.path.realpath(allowed_root or os.getcwd())

    def run(
        self,
        query: str,
        directory: str = ".",
        file_pattern: Optional[str] = None,
        max_results: int = 20,
    ) -> ToolResult:
        try:
            if not query:
                return ToolResult(success=False, error="query must be a non-empty string")

            if not is_within_allowed_root(directory, self.allowed_root):
                return ToolResult(
                    success=False,
                    error=(
                        f"Refused: '{directory}' resolves outside allowed root "
                        f"'{self.allowed_root}'"
                    ),
                )

            search_root = os.path.realpath(os.path.abspath(directory))
            if not os.path.isdir(search_root):
                return ToolResult(success=False, error=f"Not a directory: {directory}")

            max_results = max(1, int(max_results))
            matches = []
            query_lower = query.lower()
            skip_dirs = {
                ".git", "__pycache__", "node_modules", ".venv", "venv",
                "dist", "build", ".tox",
            }

            for root, dirs, files in os.walk(search_root):
                # Never walk outside sandbox even if a symlink escapes (realpath files)
                if not is_within_allowed_root(root, self.allowed_root):
                    dirs.clear()
                    continue
                dirs[:] = [d for d in dirs if d not in skip_dirs]
                for filename in files:
                    if file_pattern and not fnmatch.fnmatch(filename, file_pattern):
                        continue
                    _, ext = os.path.splitext(filename)
                    if ext.lower() in self._SKIP_EXT:
                        continue
                    filepath = os.path.join(root, filename)
                    if not is_within_allowed_root(filepath, self.allowed_root):
                        continue
                    try:
                        if os.path.getsize(filepath) > self._MAX_FILE_BYTES:
                            continue
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            for line_num, line in enumerate(f, 1):
                                if query_lower in line.lower():
                                    matches.append({
                                        "file": filepath,
                                        "line": line_num,
                                        "content": line.strip()[:500],
                                    })
                                    if len(matches) >= max_results:
                                        break
                    except (OSError, UnicodeError):
                        continue
                    if len(matches) >= max_results:
                        break
                if len(matches) >= max_results:
                    break

            return ToolResult(success=True, output=matches)
        except Exception as e:
            return ToolResult(success=False, error=str(e))
