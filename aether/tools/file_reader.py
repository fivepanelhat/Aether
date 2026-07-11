"""
File Reader Tool (hardened)

- max_lines no longer raises StopIteration on short files
- Size guard so the agent can't blow out context on huge files
- Path sandbox: refuses reads outside allowed root (default: CWD)
- Refuses symlink targets (same policy as file_writer)
"""

from .base import Tool, ToolResult
from typing import Optional
from itertools import islice
import os

from aether.paths import is_within_allowed_root

MAX_BYTES_DEFAULT = 512_000  # 500 KB safety ceiling


class FileReaderTool(Tool):
    name = "file_reader"
    description = "Read the contents of a file inside the allowed root."
    input_schema = {
        "file_path": "Path to the file (must resolve inside the allowed root)",
        "max_lines": "Optional maximum lines to read",
    }

    def __init__(self, allowed_root: str = None):
        self.allowed_root = os.path.realpath(allowed_root or os.getcwd())

    def run(self, file_path: str, max_lines: Optional[int] = None) -> ToolResult:
        try:
            if not is_within_allowed_root(file_path, self.allowed_root):
                return ToolResult(
                    success=False,
                    error=f"Refused: '{file_path}' resolves outside allowed root '{self.allowed_root}'",
                )

            if os.path.islink(file_path):
                return ToolResult(success=False, error=f"Refused: '{file_path}' is a symlink")

            if not os.path.exists(file_path):
                return ToolResult(success=False, error=f"File not found: {file_path}")

            size = os.path.getsize(file_path)
            if size > MAX_BYTES_DEFAULT and not max_lines:
                return ToolResult(
                    success=False,
                    error=f"File is {size} bytes (> {MAX_BYTES_DEFAULT}). Pass max_lines to read a portion.",
                )

            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                if max_lines:
                    content = "".join(islice(f, max_lines))
                else:
                    content = f.read()

            return ToolResult(success=True, output=content)
        except Exception as e:
            return ToolResult(success=False, error=str(e))
