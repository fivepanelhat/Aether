"""
File Reader Tool
"""

from .base import Tool, ToolResult
from typing import Optional
import os


class FileReaderTool(Tool):
    name = "file_reader"
    description = "Read the contents of a file from the filesystem."
    input_schema = {
        "file_path": "Path to the file",
        "max_lines": "Optional maximum lines to read"
    }

    def run(self, file_path: str, max_lines: Optional[int] = None) -> ToolResult:
        try:
            if not os.path.exists(file_path):
                return ToolResult(success=False, error=f"File not found: {file_path}")

            with open(file_path, "r", encoding="utf-8") as f:
                if max_lines:
                    lines = [next(f) for _ in range(max_lines)]
                    content = "".join(lines)
                else:
                    content = f.read()

            return ToolResult(success=True, output=content)
        except Exception as e:
            return ToolResult(success=False, error=str(e))
