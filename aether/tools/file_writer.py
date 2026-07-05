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
File Writer Tool (with safety considerations)
"""

from .base import Tool, ToolResult
from typing import Optional
import os


class FileWriterTool(Tool):
    name = "file_writer"
    description = "Write or overwrite a file. Use with caution — preferably after human approval."
    input_schema = {
        "file_path": "Path to write to",
        "content": "Content to write",
        "mode": "write (overwrite) or append"
    }

    def run(self, file_path: str, content: str, mode: str = "write") -> ToolResult:
        try:
            # Safety: Only allow writing inside allowed directories in future
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            write_mode = "w" if mode == "write" else "a"

            with open(file_path, write_mode, encoding="utf-8") as f:
                f.write(content)

            return ToolResult(
                success=True,
                output=f"Successfully wrote to {file_path}",
                metadata={"file_path": file_path, "bytes_written": len(content)}
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))
