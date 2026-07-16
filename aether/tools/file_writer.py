"""
File Writer Tool (hardened)

- Handles bare filenames (no dirname) without crashing
- Blocks path traversal outside the allowed root (default: CWD)
- Refuses symlink targets
"""

from .base import Tool, ToolResult
import os

from aether.paths import is_within_allowed_root


class FileWriterTool(Tool):
    name = "file_writer"
    description = "Write or overwrite a file inside the allowed root. High-risk: requires human approval."
    input_schema = {
        "file_path": "Path to write to (must resolve inside the allowed root)",
        "content": "Content to write",
        "mode": "write (overwrite) or append"
    }

    def __init__(self, allowed_root: str = None):
        # Default sandbox: the current working directory at construction time
        self.allowed_root = os.path.realpath(allowed_root or os.getcwd())

    def run(self, file_path: str, content: str, mode: str = "write") -> ToolResult:
        try:
            if mode not in ("write", "append"):
                return ToolResult(success=False, error=f"Invalid mode: {mode}")

            if not is_within_allowed_root(file_path, self.allowed_root):
                return ToolResult(
                    success=False,
                    error=f"Refused: '{file_path}' resolves outside allowed root '{self.allowed_root}'"
                )

            if os.path.islink(file_path):
                return ToolResult(success=False, error=f"Refused: '{file_path}' is a symlink")

            parent = os.path.dirname(os.path.abspath(file_path))
            os.makedirs(parent, exist_ok=True)

            write_mode = "w" if mode == "write" else "a"
            with open(file_path, write_mode, encoding="utf-8") as f:
                f.write(content)

            return ToolResult(
                success=True,
                output=f"Successfully wrote to {file_path}",
                metadata={"file_path": file_path, "bytes_written": len(content.encode('utf-8'))}
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))
