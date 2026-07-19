"""
Aether Guardrails Module (Strengthened)

Provides security, safety, cultural, and process guardrails for the orchestrator.
"""

import logging
import re
import unicodedata
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass

logger = logging.getLogger("AetherGuardrails")


@dataclass
class RiskAssessment:
    risk_level: str          # low | medium | high | critical
    reasons: List[str]
    requires_hitl: bool
    cultural_sensitivity: str  # low | medium | high


class Guardrails:
    def __init__(self):
        # High-risk keywords that trigger stronger scrutiny
        self.high_risk_keywords = [
            "health", "medical", "diagnosis", "treatment",
            "funding", "winz", "benefit", "personal data",
            "delete", "remove", "destroy", "admin", "service_role"
        ]

        # Culturally sensitive keywords
        self.cultural_keywords = [
            "maori", "whanau", "cultural", "te reo", "tikanga",
            "marae", "hapu", "iwi", "community", "indigenous"
        ]

        # Actions that should almost always require human approval
        self.always_require_approval = {
            "file_writer", "git_commit", "git_push", "deploy",
            "delete_data", "modify_user", "service_role_action"
        }

    # ==================== Core Risk Assessment ====================

    def assess_risk(self, action: str, context: str = "", metadata: Optional[Dict[str, Any]] = None) -> RiskAssessment:
        """
        Assess the risk level of an action or decision.
        """
        reasons = []
        risk_score = 0
        metadata = metadata or {}

        action_lower = action.lower()
        context_lower = context.lower()

        # Check for high-risk keywords
        for keyword in self.high_risk_keywords:
            if keyword in action_lower or keyword in context_lower:
                risk_score += 2
                reasons.append(f"Contains high-risk keyword: '{keyword}'")

        # Check for cultural sensitivity
        cultural_score = 0
        for keyword in self.cultural_keywords:
            if keyword in action_lower or keyword in context_lower:
                cultural_score += 1
                reasons.append(f"Contains culturally relevant term: '{keyword}'")

        cultural_sensitivity = "low"
        if cultural_score >= 2:
            cultural_sensitivity = "high"
        elif cultural_score == 1:
            cultural_sensitivity = "medium"

        # Check if action is in the always-require-approval list
        requires_hitl = action in self.always_require_approval

        # Determine final risk level
        if risk_score >= 5 or requires_hitl:
            risk_level = "critical"
            requires_hitl = True
        elif risk_score >= 3:
            risk_level = "high"
            requires_hitl = True
        elif risk_score >= 1:
            risk_level = "medium"
        else:
            risk_level = "low"

        assessment = RiskAssessment(
            risk_level=risk_level,
            reasons=reasons,
            requires_hitl=requires_hitl,
            cultural_sensitivity=cultural_sensitivity
        )

        logger.info(f"Risk Assessment for '{action}': {risk_level} (HITL: {requires_hitl})")
        return assessment

    # ==================== Plan & Change Validation ====================

    def check_plan(self, plan: List[str], goal: str) -> Tuple[bool, List[str]]:
        issues = []
        full_text = " ".join(plan).lower() + " " + goal.lower()

        if "bypass" in full_text or "skip approval" in full_text:
            issues.append("Plan attempts to bypass approval gates.")

        if any(kw in full_text for kw in self.high_risk_keywords):
            if "disclaimer" not in full_text and "human review" not in full_text:
                issues.append("High-risk content detected without clear human review step.")

        return len(issues) == 0, issues

    def check_change_proposal(self, change: Dict[str, Any]) -> Tuple[bool, List[str]]:
        issues = []
        description = change.get("description", "").lower()

        if any(kw in description for kw in self.high_risk_keywords):
            if not change.get("cultural_notes") and not change.get("disclaimer"):
                issues.append("High-risk change is missing cultural notes or disclaimer.")

        return len(issues) == 0, issues

    # ==================== Action-Level Checks ====================

    def should_block_action(self, action: str, context: str = "") -> bool:
        """Returns True if the action should be blocked entirely (no HITL path).

        Currently reserved for future hard-deny policy. High/critical actions
        go through HITL via enforce_hitl() rather than silent block.
        """
        assessment = self.assess_risk(action, context)
        # Hard-block only if we ever mark something critical without an approval path.
        return assessment.risk_level == "critical" and not assessment.requires_hitl

    def enforce_hitl(self, action: str, context: str = "") -> bool:
        """Returns True if this action requires human approval."""
        assessment = self.assess_risk(action, context)
        return assessment.requires_hitl or assessment.risk_level in ["high", "critical"]

    # ==================== Cultural Safety ====================

    def assess_cultural_sensitivity(self, content: str) -> str:
        """Returns low | medium | high based on cultural relevance."""
        content_lower = content.lower()
        score = sum(1 for kw in self.cultural_keywords if kw in content_lower)

        if score >= 2:
            return "high"
        elif score == 1:
            return "medium"
        return "low"

    # ==================== Input Handling (boundary-safe) ====================
    #
    # Principle: never mutate user or agent content — it corrupts legitimate
    # code, te reo, and skill bodies. Instead, escape at the exact boundary
    # where the text is used (shell, SQL, prompt), and *detect* injection
    # attempts so they can be flagged for HITL review rather than silently
    # rewritten.

    INJECTION_PATTERNS = [
        "ignore previous instructions",
        "ignore all previous",
        "ignore prior instructions",
        "ignore the above",
        "ignore your instructions",
        "disregard your instructions",
        "disregard previous instructions",
        "disregard all previous",
        "forget previous instructions",
        "forget everything above",
        "you are now",
        "you must now",
        "system prompt",
        "reveal your prompt",
        "print your instructions",
        "repeat the words above",
        "bypass approval",
        "skip approval",
        "developer mode",
        "do anything now",
        "new instructions:",
    ]

    def escape_for_shell(self, text: str) -> str:
        """Safely quote text for use as a single shell argument.

        - POSIX: ``shlex.quote`` (single-quoted)
        - Windows: ``subprocess.list2cmdline`` (CreateProcess / cmd-safe)
        Content is preserved; the shell treats it as inert data.
        """
        import os
        import shlex
        import subprocess

        if os.name == "nt":
            return subprocess.list2cmdline([text])
        return shlex.quote(text)

    @staticmethod
    def _normalize_for_screening(text: str) -> str:
        """Fold text for injection screening: convert every whitespace run to a
        single space, drop zero-width / format / control characters used to hide
        trigger phrases (e.g. ``ignore​previous``), and lowercase."""
        out = []
        for ch in str(text):
            if ch.isspace():
                out.append(" ")
            elif unicodedata.category(ch) in ("Cf", "Cc"):
                continue  # zero-width space/joiner, BOM, other invisibles
            else:
                out.append(ch)
        return re.sub(r"\s+", " ", "".join(out)).strip().lower()

    def detect_prompt_injection(self, text: str) -> Tuple[bool, List[str]]:
        """Heuristic prompt-injection detection. Returns (suspicious, matched
        patterns).

        Best-effort screening only — it is deliberately bypassable and is NOT
        the primary control. The real control is HITL routing: a flagged goal
        locks the orchestrator loop to human approval (see
        ``orchestrator._approve_if_needed``); suspicious input is routed for
        approval, never silently mutated. Normalisation resists trivial evasion
        via irregular whitespace, newlines, and zero-width characters, and
        matching also compares a whitespace-stripped form so a phrase whose
        spaces were replaced by invisibles (``ignore​previous``) still
        matches."""
        normalized = self._normalize_for_screening(text)
        despaced = normalized.replace(" ", "")
        matches = [
            p for p in self.INJECTION_PATTERNS
            if p in normalized or p.replace(" ", "") in despaced
        ]
        return (len(matches) > 0, matches)

    def sanitize_input(self, text: str) -> str:
        """DEPRECATED: kept for backwards compatibility. No longer strips
        characters (that corrupted legitimate content). Use escape_for_shell()
        at execution boundaries and detect_prompt_injection() for screening."""
        import logging as _logging
        _logging.getLogger("AetherGuardrails").warning(
            "sanitize_input is deprecated; use escape_for_shell / detect_prompt_injection"
        )
        return text.strip()
