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
Computer-use tools exposed to Aether's ReAct orchestrator.

Every tool here actuates the real machine, so all of them are declared
high-risk and are gated by Aether's guardrails / HITL layer (see
``Guardrails.always_require_approval``). The tools stay stateless; they read the
process-wide backend singleton from ``aether.computer.backend``.
"""

from __future__ import annotations

import os
import shlex
import subprocess
import tempfile
from typing import Optional

from aether.tools.base import Tool, ToolResult
from .backend import BackendUnavailable, get_backend


class _ComputerTool(Tool):
    """Shared helpers for the desktop actuators."""

    def _backend(self):
        return get_backend()

    def _guard(self) -> Optional[ToolResult]:
        be = self._backend()
        if not be.available():
            return ToolResult(
                success=False,
                error=be.unavailable_reason() or "Computer-use backend unavailable.",
            )
        return None


class ScreenshotTool(_ComputerTool):
    name = "screenshot"
    description = (
        "Capture the current screen to a PNG and return its path + dimensions. "
        "Use this to see the desktop before deciding where to click or type."
    )
    input_schema = {"path": "Optional file path for the PNG (default: temp file)"}

    def run(self, path: Optional[str] = None, **_) -> ToolResult:
        guard = self._guard()
        if guard:
            return guard
        try:
            if not path:
                fd, path = tempfile.mkstemp(prefix="aether_screen_", suffix=".png")
                os.close(fd)
            grab = self._backend().screenshot(path=path)
            return ToolResult(
                success=True,
                output=f"Captured {grab.width}x{grab.height} screenshot to {grab.path}",
                metadata={
                    "path": grab.path,
                    "width": grab.width,
                    "height": grab.height,
                },
            )
        except BackendUnavailable as exc:
            return ToolResult(success=False, error=str(exc))
        except Exception as exc:
            return ToolResult(success=False, error=f"Screenshot failed: {exc}")


class ScreenInfoTool(_ComputerTool):
    name = "screen_info"
    description = "Report screen resolution and current cursor position."
    input_schema = {}

    def run(self, **_) -> ToolResult:
        guard = self._guard()
        if guard:
            return guard
        try:
            be = self._backend()
            w, h = be.screen_size()
            cx, cy = be.cursor_position()
            return ToolResult(
                success=True,
                output=f"Screen {w}x{h}; cursor at ({cx},{cy})",
                metadata={"width": w, "height": h, "cursor": [cx, cy]},
            )
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))


class ClickTool(_ComputerTool):
    name = "computer_click"
    description = (
        "Move the pointer to absolute pixel (x, y) and click. High-risk: requires approval. "
        "button=left|right|middle, clicks=1..3."
    )
    input_schema = {
        "x": "Absolute X pixel",
        "y": "Absolute Y pixel",
        "button": "left | right | middle (default left)",
        "clicks": "1, 2 (double) or 3 (default 1)",
    }

    def run(self, x=None, y=None, button: str = "left", clicks: int = 1, **_) -> ToolResult:
        guard = self._guard()
        if guard:
            return guard
        if x is None or y is None:
            return ToolResult(success=False, error="computer_click requires 'x' and 'y'.")
        try:
            cx, cy = self._backend().click(int(x), int(y), button=str(button), clicks=int(clicks))
            return ToolResult(
                success=True,
                output=f"Clicked {button} x{clicks} at ({cx},{cy})",
                metadata={"x": cx, "y": cy, "button": button, "clicks": int(clicks)},
            )
        except Exception as exc:
            return ToolResult(success=False, error=f"Click failed: {exc}")


class MoveTool(_ComputerTool):
    name = "computer_move"
    description = "Move the pointer to absolute pixel (x, y) without clicking. High-risk."
    input_schema = {"x": "Absolute X pixel", "y": "Absolute Y pixel"}

    def run(self, x=None, y=None, **_) -> ToolResult:
        guard = self._guard()
        if guard:
            return guard
        if x is None or y is None:
            return ToolResult(success=False, error="computer_move requires 'x' and 'y'.")
        try:
            cx, cy = self._backend().move(int(x), int(y))
            return ToolResult(success=True, output=f"Moved to ({cx},{cy})", metadata={"x": cx, "y": cy})
        except Exception as exc:
            return ToolResult(success=False, error=f"Move failed: {exc}")


class TypeTool(_ComputerTool):
    name = "computer_type"
    description = "Type a string of text at the current focus. High-risk: requires approval."
    input_schema = {"text": "The literal text to type"}

    def run(self, text: Optional[str] = None, **_) -> ToolResult:
        guard = self._guard()
        if guard:
            return guard
        if text is None:
            return ToolResult(success=False, error="computer_type requires 'text'.")
        try:
            n = self._backend().type_text(str(text))
            return ToolResult(success=True, output=f"Typed {n} characters", metadata={"chars": n})
        except Exception as exc:
            return ToolResult(success=False, error=f"Type failed: {exc}")


class KeyTool(_ComputerTool):
    name = "computer_key"
    description = (
        "Press a key or chord, e.g. keys='enter' or keys='ctrl+s' or keys=['ctrl','shift','t']. "
        "High-risk: requires approval."
    )
    input_schema = {"keys": "A key name, '+'-joined chord, or list of key names"}

    def run(self, keys=None, **_) -> ToolResult:
        guard = self._guard()
        if guard:
            return guard
        if not keys:
            return ToolResult(success=False, error="computer_key requires 'keys'.")
        if isinstance(keys, str):
            key_list = [k for k in keys.replace(" ", "").split("+") if k]
        elif isinstance(keys, (list, tuple)):
            key_list = [str(k) for k in keys]
        else:
            return ToolResult(success=False, error="'keys' must be a string or list.")
        try:
            pressed = self._backend().press(key_list)
            return ToolResult(
                success=True,
                output=f"Pressed {'+'.join(pressed)}",
                metadata={"keys": pressed},
            )
        except Exception as exc:
            return ToolResult(success=False, error=f"Key press failed: {exc}")


class ScrollTool(_ComputerTool):
    name = "computer_scroll"
    description = "Scroll the wheel by 'amount' clicks (positive=up, negative=down). High-risk."
    input_schema = {
        "amount": "Wheel clicks; positive up, negative down",
        "x": "Optional X to move to first",
        "y": "Optional Y to move to first",
    }

    def run(self, amount=None, x=None, y=None, **_) -> ToolResult:
        guard = self._guard()
        if guard:
            return guard
        if amount is None:
            return ToolResult(success=False, error="computer_scroll requires 'amount'.")
        try:
            xi = int(x) if x is not None else None
            yi = int(y) if y is not None else None
            self._backend().scroll(int(amount), x=xi, y=yi)
            return ToolResult(success=True, output=f"Scrolled {amount}", metadata={"amount": int(amount)})
        except Exception as exc:
            return ToolResult(success=False, error=f"Scroll failed: {exc}")


class ShellExecTool(Tool):
    """
    Cross-platform command runner. Uses the native shell (cmd/powershell on
    Windows, /bin/sh on POSIX). High-risk and non-cached. A configurable
    timeout and output cap keep a runaway command from hanging the agent.
    """

    name = "shell_exec"
    description = (
        "Run a shell command on the local machine and capture stdout/stderr. "
        "High-risk: requires approval. Windows uses cmd, POSIX uses /bin/sh."
    )
    input_schema = {
        "command": "The command line to execute",
        "cwd": "Optional working directory",
        "timeout": "Seconds before the command is killed (default 60)",
    }

    def __init__(self, allowed_root: Optional[str] = None, max_output: int = 8000):
        self.allowed_root = os.path.realpath(allowed_root) if allowed_root else None
        self.max_output = max_output

    def run(self, command: Optional[str] = None, cwd: Optional[str] = None, timeout: int = 60, **_) -> ToolResult:
        if not command or not str(command).strip():
            return ToolResult(success=False, error="shell_exec requires 'command'.")
        workdir = cwd or self.allowed_root or os.getcwd()
        if not os.path.isdir(workdir):
            return ToolResult(success=False, error=f"Working directory does not exist: {workdir}")
        try:
            completed = subprocess.run(
                command,
                shell=True,
                cwd=workdir,
                capture_output=True,
                text=True,
                timeout=max(1, int(timeout)),
            )
            out = (completed.stdout or "")[: self.max_output]
            err = (completed.stderr or "")[: self.max_output]
            body = out
            if err:
                body += f"\n[stderr]\n{err}"
            return ToolResult(
                success=completed.returncode == 0,
                output=body.strip() or f"(exit {completed.returncode}, no output)",
                error=None if completed.returncode == 0 else f"Exit code {completed.returncode}",
                metadata={"returncode": completed.returncode, "cwd": workdir},
            )
        except subprocess.TimeoutExpired:
            return ToolResult(success=False, error=f"Command timed out after {timeout}s")
        except Exception as exc:
            return ToolResult(success=False, error=f"shell_exec failed: {exc}")


#: Names of every tool defined here — the orchestrator marks these high-risk.
COMPUTER_TOOL_NAMES = [
    "screenshot",
    "screen_info",
    "computer_click",
    "computer_move",
    "computer_type",
    "computer_key",
    "computer_scroll",
    "shell_exec",
]

#: Subset that actuates the machine (used to force HITL). ``screenshot`` and
#: ``screen_info`` are read-only observation and stay ungated.
COMPUTER_ACTUATORS = [
    "computer_click",
    "computer_move",
    "computer_type",
    "computer_key",
    "computer_scroll",
    "shell_exec",
]


def build_computer_tools(allowed_root: Optional[str] = None):
    """Instantiate every computer-use tool in registration order."""
    return [
        ScreenshotTool(),
        ScreenInfoTool(),
        ClickTool(),
        MoveTool(),
        TypeTool(),
        KeyTool(),
        ScrollTool(),
        ShellExecTool(allowed_root=allowed_root),
    ]
