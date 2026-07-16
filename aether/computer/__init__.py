# Copyright 2026 Aether Project Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Aether Computer Use - cross-platform desktop control for edge AI.

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
