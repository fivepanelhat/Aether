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
Aether Guardrails Module (Strengthened)

Provides security, safety, cultural, and process guardrails for the orchestrator.
"""

import logging
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
        """Returns True if the action should be blocked entirely."""
        assessment = self.assess_risk(action, context)
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

    # ==================== Input Sanitization (Basic) ====================

    def sanitize_input(self, text: str) -> str:
        """Basic input sanitization. Can be expanded later."""
        # Remove potential command injection characters (very basic)
        dangerous_chars = [";", "`", "$", "|", "&"]
        for char in dangerous_chars:
            text = text.replace(char, "")
        return text.strip()
