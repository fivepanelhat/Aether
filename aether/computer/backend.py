# Copyright (c) 2026 Coastal Alpine Tech Limited. All rights reserved.
# Proprietary and confidential. No open-source grant is implied by access to
# this file; use is governed solely by the LICENSE at the repository root.
"""
Cross-platform computer-use backend.

Design goals mirror the rest of Aether:
- Works on Windows and Linux (and macOS) from one code path.
- Optional heavy deps (``pyautogui``/``Pillow``) — import lazily so the base
  package still installs on headless edge nodes. Install with
  ``pip install "aether[computer]"``.
- Graceful degradation: if no display / no backend is present, the backend
  reports *unavailable* with an actionable reason instead of crashing the CLI.
- Safety first: coordinates are clamped to the real screen, the PyAutoGUI
  fail-safe (slam mouse to a corner to abort) stays ON, and a global
  ``AETHER_COMPUTER_DRY_RUN`` switch lets you rehearse an agent run without
  actuating hardware.
"""

from __future__ import annotations

import base64
import io
import logging
import os
import platform
import time
from dataclasses import dataclass
from typing import List, Optional, Tuple

logger = logging.getLogger("AetherComputer")

# Keys accepted by press()/hotkey(); superset of the pyautogui vocabulary we rely on.
COMMON_KEYS = {
    "enter", "return", "tab", "space", "backspace", "delete", "esc", "escape",
    "up", "down", "left", "right", "home", "end", "pageup", "pagedown",
    "ctrl", "control", "alt", "shift", "win", "cmd", "command", "super",
    "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
    "capslock", "insert", "printscreen",
}

VALID_BUTTONS = {"left", "right", "middle"}


class BackendUnavailable(RuntimeError):
    """Raised when desktop actuation is requested but no backend is usable."""


@dataclass
class ScreenGrab:
    """A captured frame plus the metadata a vision model / audit trail needs."""

    width: int
    height: int
    png_bytes: bytes
    path: Optional[str] = None
    captured_at: float = 0.0

    def to_base64(self) -> str:
        return base64.b64encode(self.png_bytes).decode("ascii")


def _dry_run_enabled() -> bool:
    return os.environ.get("AETHER_COMPUTER_DRY_RUN", "").strip().lower() in {"1", "true", "yes", "on"}


class ComputerBackend:
    """
    Thin, safety-wrapped facade over a desktop-automation engine.

    Currently backed by PyAutoGUI (cross-platform). The public surface is kept
    deliberately small and engine-agnostic so an alternative backend (e.g. a
    Wayland-native or RPA engine) can be dropped in later without touching the
    tools or the agent loop.
    """

    def __init__(self, move_duration: float = 0.15, dry_run: Optional[bool] = None):
        self.move_duration = max(0.0, float(move_duration))
        self.dry_run = _dry_run_enabled() if dry_run is None else bool(dry_run)
        self._pg = None  # lazily bound pyautogui module
        self._reason: Optional[str] = None
        self._size: Optional[Tuple[int, int]] = None

    # ---------------- availability ----------------

    def _load(self):
        """Import and configure the underlying engine, caching the failure reason."""
        if self._pg is not None:
            return self._pg
        if self._reason is not None:
            raise BackendUnavailable(self._reason)

        # A display is required on Linux; PyAutoGUI raises KeyError('DISPLAY') otherwise.
        if platform.system() == "Linux" and not (
            os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
        ):
            self._reason = (
                "No X11/Wayland display detected (DISPLAY unset). Computer use needs a "
                "graphical session. On a headless box run under Xvfb or a real desktop."
            )
            raise BackendUnavailable(self._reason)

        try:
            import pyautogui  # type: ignore
        except Exception as exc:  # ImportError, or platform import-time failures
            self._reason = (
                f"PyAutoGUI backend unavailable ({exc}). Install desktop extras with: "
                'pip install "aether[computer]"'
            )
            raise BackendUnavailable(self._reason) from exc

        # Keep the fail-safe ON: flinging the cursor to (0,0) aborts automation.
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.05
        self._pg = pyautogui
        return self._pg

    def available(self) -> bool:
        try:
            self._load()
            return True
        except BackendUnavailable:
            return False

    def unavailable_reason(self) -> Optional[str]:
        if self.available():
            return None
        return self._reason

    # ---------------- geometry ----------------

    def screen_size(self) -> Tuple[int, int]:
        pg = self._load()
        size = pg.size()
        self._size = (int(size[0]), int(size[1]))
        return self._size

    def _clamp(self, x: int, y: int) -> Tuple[int, int]:
        w, h = self.screen_size()
        cx = max(0, min(int(x), w - 1))
        cy = max(0, min(int(y), h - 1))
        if (cx, cy) != (int(x), int(y)):
            logger.debug("Clamped (%s,%s) -> (%s,%s) within %sx%s", x, y, cx, cy, w, h)
        return cx, cy

    def cursor_position(self) -> Tuple[int, int]:
        pg = self._load()
        pos = pg.position()
        return int(pos[0]), int(pos[1])

    # ---------------- capture ----------------

    def screenshot(self, path: Optional[str] = None) -> ScreenGrab:
        pg = self._load()
        img = pg.screenshot()
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        png = buf.getvalue()
        if path:
            with open(path, "wb") as fh:
                fh.write(png)
        return ScreenGrab(
            width=int(img.width),
            height=int(img.height),
            png_bytes=png,
            path=path,
            captured_at=time.time(),
        )

    # ---------------- pointer ----------------

    def move(self, x: int, y: int) -> Tuple[int, int]:
        pg = self._load()
        cx, cy = self._clamp(x, y)
        if not self.dry_run:
            pg.moveTo(cx, cy, duration=self.move_duration)
        return cx, cy

    def click(self, x: int, y: int, button: str = "left", clicks: int = 1) -> Tuple[int, int]:
        pg = self._load()
        button = button.lower()
        if button not in VALID_BUTTONS:
            raise ValueError(f"Invalid button '{button}'. Use one of {sorted(VALID_BUTTONS)}.")
        clicks = max(1, min(int(clicks), 3))
        cx, cy = self._clamp(x, y)
        if not self.dry_run:
            pg.moveTo(cx, cy, duration=self.move_duration)
            pg.click(clicks=clicks, button=button)
        return cx, cy

    def double_click(self, x: int, y: int, button: str = "left") -> Tuple[int, int]:
        return self.click(x, y, button=button, clicks=2)

    def scroll(self, amount: int, x: Optional[int] = None, y: Optional[int] = None) -> None:
        pg = self._load()
        if x is not None and y is not None:
            cx, cy = self._clamp(x, y)
            if not self.dry_run:
                pg.moveTo(cx, cy, duration=self.move_duration)
        if not self.dry_run:
            pg.scroll(int(amount))

    def drag(self, x1: int, y1: int, x2: int, y2: int, button: str = "left") -> Tuple[int, int]:
        pg = self._load()
        button = button.lower()
        if button not in VALID_BUTTONS:
            raise ValueError(f"Invalid button '{button}'.")
        sx, sy = self._clamp(x1, y1)
        ex, ey = self._clamp(x2, y2)
        if not self.dry_run:
            pg.moveTo(sx, sy, duration=self.move_duration)
            pg.dragTo(ex, ey, duration=max(0.2, self.move_duration), button=button)
        return ex, ey

    # ---------------- keyboard ----------------

    def type_text(self, text: str, interval: float = 0.01) -> int:
        pg = self._load()
        text = str(text)
        if not self.dry_run:
            pg.typewrite(text, interval=max(0.0, float(interval)))
        return len(text)

    def press(self, keys: List[str]) -> List[str]:
        """Press one key, or a chord when multiple keys are given (hotkey)."""
        pg = self._load()
        norm = [self._normalise_key(k) for k in keys if str(k).strip()]
        if not norm:
            raise ValueError("No key specified.")
        if not self.dry_run:
            if len(norm) == 1:
                pg.press(norm[0])
            else:
                pg.hotkey(*norm)
        return norm

    @staticmethod
    def _normalise_key(key: str) -> str:
        k = str(key).strip().lower()
        aliases = {
            "control": "ctrl",
            "return": "enter",
            "escape": "esc",
            "command": "cmd",
            "super": "win",
            "windows": "win",
        }
        return aliases.get(k, k)


# Module-level singleton so tools and the agent share one configured backend.
_BACKEND: Optional[ComputerBackend] = None


def get_backend(force_new: bool = False, **kwargs) -> ComputerBackend:
    global _BACKEND
    if _BACKEND is None or force_new:
        _BACKEND = ComputerBackend(**kwargs)
    return _BACKEND


def backend_status() -> dict:
    """Machine-readable readiness report for ``aether doctor``."""
    be = get_backend()
    status = {
        "platform": platform.system(),
        "python": platform.python_version(),
        "dry_run": be.dry_run,
        "available": False,
        "reason": None,
        "screen": None,
    }
    if be.available():
        status["available"] = True
        try:
            w, h = be.screen_size()
            status["screen"] = f"{w}x{h}"
        except Exception as exc:  # capture backend that imports but can't size
            status["available"] = False
            status["reason"] = str(exc)
    else:
        status["reason"] = be.unavailable_reason()
    return status
