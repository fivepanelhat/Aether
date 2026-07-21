# Copyright (c) 2026 Coastal Alpine Tech Limited. All rights reserved.
# Proprietary and confidential. No open-source grant is implied by access to
# this file; use is governed solely by the LICENSE at the repository root.
"""
Aether Computer Use — cross-platform desktop control for edge AI.

Adds screenshot, pointer, keyboard, and shell actuation on top of Aether's
sovereign ReAct orchestrator so a local (Ollama) vision model can operate a
real Windows or Linux desktop. Every actuator is treated as a high-risk tool
and routed through Aether's guardrails / human-in-the-loop gates.
"""

from .backend import (
    ComputerBackend,
    BackendUnavailable,
    ScreenGrab,
    get_backend,
    backend_status,
)

__all__ = [
    "ComputerBackend",
    "BackendUnavailable",
    "ScreenGrab",
    "get_backend",
    "backend_status",
]
