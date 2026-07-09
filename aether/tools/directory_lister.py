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
Directory Lister Tool
"""

from .base import Tool, ToolResult
import os


class DirectoryListerTool(Tool):
    name = "directory_lister"
    description = "List files and directories in a given path. Useful for project exploration."
    input_schema = {
        "path": "Directory to list (default: current directory). Alias: directory",
        "max_depth": "Recursion depth (default: 1)",
    }

    def run(self, path: str = ".", max_depth: int = 1, directory: str = None, **kwargs) -> ToolResult:
        # Accept both "path" and "directory" (LLM / pipeline often pass directory=)
        target = directory if directory is not None else path
        if target is None or target == "":
            target = "."

        try:
            max_depth = int(max_depth) if max_depth is not None else 1
            if max_depth < 0:
                max_depth = 0

            if not os.path.exists(target):
                return ToolResult(success=False, error=f"Path does not exist: {target}")

            if not os.path.isdir(target):
                return ToolResult(success=False, error=f"Not a directory: {target}")

            result_lines = []
            # Normalize for depth calculation across OS path styles
            base = os.path.abspath(target)
            for root, dirs, files in os.walk(base):
                level = os.path.relpath(root, base).count(os.sep)
                if root == base:
                    level = 0
                if level > max_depth:
                    dirs.clear()
                    continue
                indent = "  " * level
                result_lines.append(f"{indent}{os.path.basename(root) or root}/")
                if level >= max_depth:
                    dirs.clear()
                    continue
                sub_indent = "  " * (level + 1)
                for file in files:
                    result_lines.append(f"{sub_indent}{file}")

            return ToolResult(success=True, output="\n".join(result_lines))

        except Exception as e:
            return ToolResult(success=False, error=str(e))
