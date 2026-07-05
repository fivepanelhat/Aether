"""
Aether LLM Module — Ollama integration (Phase C)

Design goals:
- stdlib only (urllib), no new dependencies — suits edge/sovereign deployment
- Graceful degradation: if Ollama is unreachable, orchestrator falls back
  to the deterministic pipeline
- Strict JSON action contract with validation against the tool/skill registry
- Injectable transport for offline unit testing
"""

import json
import logging
import time
import urllib.request
import urllib.error
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("AetherLLM")

DEFAULT_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5-coder:7b"  # solid tool-use model for Pi 5 / Hailo-class hardware; override via config


@dataclass
class LLMDecision:
    thought: str
    action: str                      # tool name | skill name | "conclude"
    args: Dict[str, Any]
    raw: str = ""
    valid: bool = True
    error: Optional[str] = None


class OllamaClient:
    """
    Minimal Ollama chat client.

    transport: optional callable (url, payload_dict, timeout) -> response_text.
    Used in tests to avoid network calls; defaults to urllib POST.
    """

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        model: str = DEFAULT_MODEL,
        timeout: int = 60,
        max_retries: int = 2,
        transport: Optional[Callable[[str, Dict[str, Any], int], str]] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
        self._transport = transport or self._http_post

    # ---------------- transport ----------------

    def _http_post(self, url: str, payload: Dict[str, Any], timeout: int) -> str:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data, headers={"Content-Type": "application/json"}, method="POST"
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")

    def is_available(self) -> bool:
        """Cheap health check — used by the orchestrator to decide LLM vs fallback."""
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=3) as resp:
                return resp.status == 200
        except Exception:
            return False

    # ---------------- chat ----------------

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.2) -> str:
        """Single chat completion with retry + exponential backoff."""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature},
        }
        url = f"{self.base_url}/api/chat"

        last_error: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                raw = self._transport(url, payload, self.timeout)
                body = json.loads(raw)
                content = body.get("message", {}).get("content", "")
                if not content:
                    raise ValueError("Empty completion from Ollama")
                return content
            except Exception as e:
                last_error = e
                wait = 2 ** attempt
                logger.warning(f"LLM call failed (attempt {attempt + 1}): {e}. Retrying in {wait}s")
                if attempt < self.max_retries:
                    time.sleep(wait)

        raise RuntimeError(f"Ollama unavailable after {self.max_retries + 1} attempts: {last_error}")


# ---------------- ReAct prompting ----------------

SYSTEM_PROMPT = """You are Aether, a sovereign agentic development orchestrator operating under \
Te Tiriti o Waitangi and Te Mana Raraunga principles. You decide ONE next action per turn.

Rules:
- Respond with ONLY a JSON object. No markdown fences, no prose outside the JSON.
- Schema: {"thought": "<brief reasoning>", "action": "<one of the allowed actions>", "args": {}}
- "action" MUST be exactly one of the allowed tool names, skill names, or "conclude".
- High-risk actions (file writes, deploys) are gated by human approval downstream — never try to bypass this.
- If the goal touches Maori data, whanau, marae, or community contexts, note this in "thought" so \
cultural review is triggered.
- When you have enough information to answer the goal, choose "conclude" and summarise in "thought".
"""


def build_react_messages(
    goal: str,
    state_summary: str,
    tool_descriptions: str,
    skill_descriptions: str,
    observations: List[str],
) -> List[Dict[str, str]]:
    obs_text = "\n".join(observations[-6:]) if observations else "None yet."
    user = f"""GOAL: {goal}

CURRENT STATE:
{state_summary}

ALLOWED TOOLS:
{tool_descriptions}

ALLOWED SKILLS:
{skill_descriptions}

RECENT OBSERVATIONS:
{obs_text}

Decide the single next action. JSON only."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user},
    ]


def parse_decision(raw: str, allowed_actions: List[str]) -> LLMDecision:
    """
    Parse and validate the model's JSON decision.
    Tolerates accidental markdown fences; rejects anything not in the allowlist.
    """
    text = raw.strip()
    if text.startswith("```"):
        # strip ```json ... ``` fences
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return LLMDecision(
            thought="", action="conclude", args={}, raw=raw,
            valid=False, error=f"Invalid JSON from model: {e}"
        )

    action = str(data.get("action", "")).strip()
    thought = str(data.get("thought", "")).strip()
    args = data.get("args", {})
    if not isinstance(args, dict):
        args = {}

    if action not in allowed_actions:
        return LLMDecision(
            thought=thought, action="conclude", args={}, raw=raw,
            valid=False, error=f"Model chose disallowed action '{action}'"
        )

    return LLMDecision(thought=thought, action=action, args=args, raw=raw)
