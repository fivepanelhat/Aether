"""
Aether Guardrails Module

Central place for safety, cultural, and process guardrails.
"""

from typing import List, Dict, Any, Tuple


class Guardrails:
    def __init__(self):
        self.high_risk_keywords = [
            "health", "medical", "diagnosis", "treatment",
            "funding", "winz", "benefit", "personal data"
        ]

    def check_plan(self, plan: List[str], goal: str) -> Tuple[bool, List[str]]:
        issues = []
        plan_text = " ".join(plan).lower() + " " + goal.lower()

        if "bypass" in plan_text or "skip approval" in plan_text:
            issues.append("Plan appears to bypass approval gates.")

        if any(kw in plan_text for kw in self.high_risk_keywords):
            if "disclaimer" not in plan_text:
                issues.append("High-risk content detected without disclaimer step.")

        return len(issues) == 0, issues

    def check_change_proposal(self, change: Dict[str, Any]) -> Tuple[bool, List[str]]:
        issues = []
        description = change.get("description", "").lower()

        if any(kw in description for kw in self.high_risk_keywords):
            if not change.get("cultural_notes"):
                issues.append("High-risk change missing cultural notes.")

        return len(issues) == 0, issues

    def enforce_hitl(self, action_type: str) -> bool:
        high_risk = ["git_commit", "git_push", "pr_create", "deploy"]
        return action_type in high_risk
