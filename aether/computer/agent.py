# Copyright (c) 2026 Coastal Alpine Tech Limited. All rights reserved.
# Proprietary and confidential. No open-source grant is implied by access to
# this file; use is governed solely by the LICENSE at the repository root.
"""
Vision computer-use agent.

A screenshot -> decide -> act loop driven by a *local* multimodal Ollama model.
Each turn:

  1. Capture the screen and send it (base64) to the vision model with the goal.
  2. Parse a single strict-JSON action (click/type/key/scroll/screenshot/done).
  3. Screen the model's reasoning for prompt-injection.
  4. Route any actuating step through Aether's guardrails / human approval.
  5. Execute via the shared computer backend and feed the result back.

Everything runs on-device: no screenshots or keystrokes leave the machine.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from aether.guardrails import Guardrails
from aether.llm import OllamaClient
from .backend import BackendUnavailable, get_backend

logger = logging.getLogger("AetherComputerAgent")

DEFAULT_VISION_MODEL = "qwen2.5-vl:7b"

VISION_SYSTEM_PROMPT = """You are Aether Computer Use, a sovereign on-device agent that operates a real \
desktop by looking at screenshots. You act under Te Tiriti o Waitangi and Te Mana Raraunga data-sovereignty \
principles: everything stays local and you never exfiltrate data.

You are shown a screenshot of the current screen (its pixel size is given). Decide the SINGLE next action \
that best advances the goal.

Respond with ONLY a JSON object, no markdown fences, no prose. Schema:
{"thought": "<brief reasoning>", "action": "<action>", "args": {<...>}}

Allowed actions and args:
- "screenshot"      {}                                  # look again after a UI change
- "click"           {"x": int, "y": int, "button": "left|right|middle", "clicks": 1}
- "move"            {"x": int, "y": int}
- "type"            {"text": "<string to type>"}
- "key"             {"keys": "enter" | "ctrl+s" | ["ctrl","shift","t"]}
- "scroll"          {"amount": int}                     # positive up, negative down
- "wait"            {"seconds": number}                 # let the UI settle
- "done"            {"summary": "<what was accomplished>"}

Rules:
- Coordinates are absolute screen pixels. Aim for the centre of the target control.
- Take ONE action per turn. After an action that changes the screen, use "screenshot" to re-observe.
- If the goal is complete, choose "done" with a short summary.
- Never attempt to bypass approval prompts; a human may confirm high-risk actions.
"""

# Actions that actuate the machine and must pass the approval gate.
_ACTUATING = {"click", "move", "type", "key", "scroll"}


@dataclass
class ComputerStep:
    index: int
    thought: str
    action: str
    args: Dict[str, Any]
    result: str
    approved: bool = True


@dataclass
class ComputerRunResult:
    goal: str
    steps: List[ComputerStep] = field(default_factory=list)
    completed: bool = False
    summary: str = ""
    halted_reason: Optional[str] = None

    def render(self) -> str:
        lines = [f"Goal: {self.goal}", f"Steps: {len(self.steps)}"]
        for s in self.steps:
            gate = "" if s.approved else " [DENIED]"
            lines.append(f"  {s.index}. {s.action}{gate} — {s.thought[:80]}")
            if s.result:
                lines.append(f"       -> {s.result[:120]}")
        if self.completed:
            lines.append(f"Completed: {self.summary}")
        elif self.halted_reason:
            lines.append(f"Halted: {self.halted_reason}")
        return "\n".join(lines)


class ComputerUseAgent:
    """
    Drives the vision loop. ``approver`` is called for every actuating step with
    (action, args) and must return True to proceed. Defaults to auto-approve
    only when ``auto_approve=True`` (otherwise it denies, keeping runs safe by
    default in non-interactive contexts).
    """

    def __init__(
        self,
        llm: Optional[OllamaClient] = None,
        model: str = DEFAULT_VISION_MODEL,
        base_url: str = "http://localhost:11434",
        auto_approve: bool = False,
        approver: Optional[Callable[[str, Dict[str, Any]], bool]] = None,
        guardrails: Optional[Guardrails] = None,
    ):
        self.llm = llm or OllamaClient(base_url=base_url, model=model)
        self.auto_approve = auto_approve
        self.approver = approver
        self.guardrails = guardrails or Guardrails()
        self.backend = get_backend()

    # ---------------- approval ----------------

    def _approve(self, action: str, args: Dict[str, Any]) -> bool:
        if action not in _ACTUATING:
            return True
        if self.approver is not None:
            return bool(self.approver(action, args))
        return bool(self.auto_approve)

    # ---------------- parsing ----------------

    @staticmethod
    def _parse(raw: str) -> Dict[str, Any]:
        text = raw.strip()
        if text.startswith("```"):
            text = text.strip("`")
            if text.lower().startswith("json"):
                text = text[4:]
            text = text.strip()
        # tolerate leading/trailing prose by grabbing the outermost JSON object
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end != -1 and end > start:
            text = text[start : end + 1]
        return json.loads(text)

    # ---------------- main loop ----------------

    def run(self, goal: str, max_steps: int = 12, settle: float = 0.4) -> ComputerRunResult:
        result = ComputerRunResult(goal=goal)

        if not self.backend.available():
            result.halted_reason = self.backend.unavailable_reason() or "backend unavailable"
            return result
        if not self.llm.is_available():
            result.halted_reason = (
                f"Local vision model unreachable at {self.llm.base_url}. Start Ollama and "
                f"pull a vision model, e.g. `ollama pull {self.llm.model}`."
            )
            return result

        # Screen the goal itself for injection before we start acting on a live desktop.
        suspicious, patterns = self.guardrails.detect_prompt_injection(goal)
        if suspicious:
            result.halted_reason = f"Goal flagged for injection patterns: {patterns}"
            return result

        history: List[str] = []
        for step in range(1, max_steps + 1):
            try:
                grab = self.backend.screenshot()
            except BackendUnavailable as exc:
                result.halted_reason = str(exc)
                break

            user = self._build_user_message(goal, grab.width, grab.height, history)
            messages = [
                {"role": "system", "content": VISION_SYSTEM_PROMPT},
                {"role": "user", "content": user},
            ]
            try:
                raw = self.llm.chat(messages, images=[grab.to_base64()])
                decision = self._parse(raw)
            except Exception as exc:
                logger.warning("Vision decision failed at step %s: %s", step, exc)
                history.append(f"step {step}: model returned unparseable output ({exc})")
                continue

            thought = str(decision.get("thought", "")).strip()
            action = str(decision.get("action", "")).strip().lower()
            args = decision.get("args") or {}
            if not isinstance(args, dict):
                args = {}

            inj, pats = self.guardrails.detect_prompt_injection(thought)
            if inj:
                result.halted_reason = f"Injection patterns in model reasoning: {pats}"
                break

            logger.info("[Computer] Step %s: %s %s", step, action, args)

            if action == "done":
                result.completed = True
                result.summary = str(args.get("summary", thought or "Task complete."))
                result.steps.append(ComputerStep(step, thought, action, args, result.summary))
                break

            if action == "wait":
                secs = float(args.get("seconds", 1.0))
                time.sleep(max(0.0, min(secs, 10.0)))
                result.steps.append(ComputerStep(step, thought, action, args, f"waited {secs}s"))
                history.append(f"step {step}: waited {secs}s")
                continue

            approved = self._approve(action, args)
            if not approved:
                msg = "denied by approver"
                result.steps.append(ComputerStep(step, thought, action, args, msg, approved=False))
                result.halted_reason = f"Step {step} ({action}) {msg}."
                break

            exec_result = self._execute(action, args)
            result.steps.append(ComputerStep(step, thought, action, args, exec_result, approved=True))
            history.append(f"step {step}: {action} -> {exec_result}")
            time.sleep(max(0.0, settle))
        else:
            result.halted_reason = f"Reached max_steps={max_steps} without completion."

        return result

    def _build_user_message(self, goal: str, w: int, h: int, history: List[str]) -> str:
        recent = "\n".join(history[-6:]) if history else "None yet."
        return (
            f"GOAL: {goal}\n\n"
            f"SCREEN SIZE: {w}x{h} pixels (top-left is 0,0)\n\n"
            f"RECENT ACTIONS:\n{recent}\n\n"
            "The attached image is the current screen. Decide the single next action. JSON only."
        )

    def _execute(self, action: str, args: Dict[str, Any]) -> str:
        be = self.backend
        try:
            if action == "screenshot":
                grab = be.screenshot()
                return f"observed {grab.width}x{grab.height}"
            if action == "click":
                x, y = be.click(
                    int(args["x"]), int(args["y"]),
                    button=str(args.get("button", "left")),
                    clicks=int(args.get("clicks", 1)),
                )
                return f"clicked ({x},{y})"
            if action == "move":
                x, y = be.move(int(args["x"]), int(args["y"]))
                return f"moved ({x},{y})"
            if action == "type":
                n = be.type_text(str(args.get("text", "")))
                return f"typed {n} chars"
            if action == "key":
                keys = args.get("keys", "")
                key_list = (
                    [k for k in str(keys).replace(" ", "").split("+") if k]
                    if isinstance(keys, str)
                    else [str(k) for k in keys]
                )
                pressed = be.press(key_list)
                return f"pressed {'+'.join(pressed)}"
            if action == "scroll":
                be.scroll(int(args.get("amount", 0)))
                return f"scrolled {args.get('amount', 0)}"
            return f"unknown action '{action}' ignored"
        except KeyError as exc:
            return f"missing arg {exc} for {action}"
        except Exception as exc:
            return f"{action} failed: {exc}"
