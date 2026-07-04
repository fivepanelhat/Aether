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

    def run(self, path: str = ".", max_depth: int = 1) -> ToolResult:
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
