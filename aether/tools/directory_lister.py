# Copyright (c) 2026 Coastal Alpine Tech Limited. All rights reserved.
# Proprietary and confidential. No open-source grant is implied by access to
# this file; use is governed solely by the LICENSE at the repository root.
"""
Directory Lister Tool (path-sandboxed)
"""

from .base import Tool, ToolResult
import os

from aether.paths import is_within_allowed_root


class DirectoryListerTool(Tool):
    name = "directory_lister"
    description = "List files and directories inside the allowed root."
    input_schema = {
        "path": "Directory to list (default: current directory). Alias: directory",
        "max_depth": "Recursion depth (default: 1)",
    }

    def __init__(self, allowed_root: str = None):
        self.allowed_root = os.path.realpath(allowed_root or os.getcwd())

    def run(self, path: str = ".", max_depth: int = 1, directory: str = None, **kwargs) -> ToolResult:
        # Accept both "path" and "directory" (LLM / pipeline often pass directory=)
        target = directory if directory is not None else path
        if target is None or target == "":
            target = "."

        try:
            if not is_within_allowed_root(target, self.allowed_root):
                return ToolResult(
                    success=False,
                    error=(
                        f"Refused: '{target}' resolves outside allowed root "
                        f"'{self.allowed_root}'"
                    ),
                )

            max_depth = int(max_depth) if max_depth is not None else 1
            if max_depth < 0:
                max_depth = 0

            if not os.path.exists(target):
                return ToolResult(success=False, error=f"Path does not exist: {target}")

            if not os.path.isdir(target):
                return ToolResult(success=False, error=f"Not a directory: {target}")

            result_lines = []
            base = os.path.realpath(os.path.abspath(target))
            for root, dirs, files in os.walk(base):
                if not is_within_allowed_root(root, self.allowed_root):
                    dirs.clear()
                    continue
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
