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
        "path": "Directory to list (default: current directory)",
        "max_depth": "Recursion depth (default: 1)"
    }

    def run(self, path: str = ".", max_depth: int = 1, **kwargs) -> ToolResult:
        try:
            if not os.path.exists(path):
                return ToolResult(success=False, error=f"Path does not exist: {path}")

            result_lines = []
            for root, dirs, files in os.walk(path):
                level = root.replace(path, "").count(os.sep)
                if level > max_depth:
                    continue
                indent = "  " * level
                result_lines.append(f"{indent}{os.path.basename(root)}/")
                sub_indent = "  " * (level + 1)
                for file in files:
                    result_lines.append(f"{sub_indent}{file}")

            return ToolResult(success=True, output="\n".join(result_lines))

        except Exception as e:
            return ToolResult(success=False, error=str(e))
