"""
File Reader Tool (hardened)

- max_lines no longer raises StopIteration on short files
- Adds a size guard so the agent can't blow out context on huge files
"""

from .base import Tool, ToolResult
from typing import Optional
from itertools import islice
import os

MAX_BYTES_DEFAULT = 512_000  # 500 KB safety ceiling


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

            size = os.path.getsize(file_path)
            if size > MAX_BYTES_DEFAULT and not max_lines:
                return ToolResult(
                    success=False,
                    error=f"File is {size} bytes (> {MAX_BYTES_DEFAULT}). Pass max_lines to read a portion."
                )

            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                if max_lines:
                    content = "".join(islice(f, max_lines))
                else:
                    content = f.read()

            return ToolResult(success=True, output=content)
        except Exception as e:
            return ToolResult(success=False, error=str(e))
