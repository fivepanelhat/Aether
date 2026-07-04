"""
Formal Threat Modeling for Aether

Uses a lightweight STRIDE-based model adapted for agentic systems.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger("AetherThreatModeling")


@dataclass
class Threat:
    category: str           # STRIDE category
    description: str
    severity: str           # low | medium | high | critical
    affected_component: str
    mitigation: str
    likelihood: str = "medium"


@dataclass
class ThreatModel:
    action: str
    threats: List[Threat] = field(default_factory=list)
    overall_risk: str = "low"
    requires_hitl: bool = False


class ThreatModeler:
    def __init__(self):
        self.stride_categories = [
            "Spoofing",
            "Tampering",
            "Repudiation",
            "Information Disclosure",
            "Denial of Service",
            "Elevation of Privilege"
        ]

    def analyze_action(self, action: str, context: str = "", metadata: Optional[Dict[str, Any]] = None) -> ThreatModel:
        """
        Perform formal threat modeling on a proposed action.
        """
        metadata = metadata or {}
        threats: List[Threat] = []

        action_lower = action.lower()
        context_lower = context.lower()

        # === Spoofing ===
        if any(kw in action_lower for kw in ["auth", "login", "identity", "impersonate"]):
            threats.append(Threat(
                category="Spoofing",
                description="Potential for identity spoofing or unauthorized impersonation.",
                severity="high",
                affected_component="Authentication",
                mitigation="Enforce strong authentication and role validation on all sensitive actions."
            ))

        # === Tampering ===
        if any(kw in action_lower for kw in ["write", "modify", "update", "edit", "file_writer"]):
            threats.append(Threat(
                category="Tampering",
                description="Risk of unauthorized modification of code, data, or configuration.",
                severity="high",
                affected_component="File System / Codebase",
                mitigation="Require human approval for all file modification actions. Use version control."
            ))

        # === Repudiation ===
        if any(kw in action_lower for kw in ["delete", "remove", "audit", "log"]):
            threats.append(Threat(
                category="Repudiation",
                description="Actions may not be properly logged or attributed, enabling denial of responsibility.",
                severity="medium",
                affected_component="Logging & Audit Trail",
                mitigation="Ensure all high-impact actions are logged with actor, timestamp, and context."
            ))

        # === Information Disclosure ===
        if any(kw in action_lower for kw in ["read", "export", "query", "memory", "search"]):
            threats.append(Threat(
                category="Information Disclosure",
                description="Risk of exposing sensitive data, code, or internal system information.",
                severity="high",
                affected_component="Data Access Layer",
                mitigation="Apply strict access controls and sanitize outputs. Never leak raw errors."
            ))

        # === Denial of Service ===
        if any(kw in action_lower for kw in ["deploy", "build", "heavy", "expensive", "loop"]):
            threats.append(Threat(
                category="Denial of Service",
                description="Action could consume excessive resources or cause system instability.",
                severity="medium",
                affected_component="Execution Environment",
                mitigation="Implement rate limiting, timeouts, and resource usage monitoring."
            ))

        # === Elevation of Privilege ===
        if any(kw in action_lower for kw in ["admin", "service_role", "privilege", "escalate", "root"]):
            threats.append(Threat(
                category="Elevation of Privilege",
                description="Risk of unauthorized privilege escalation or misuse of elevated access.",
                severity="critical",
                affected_component="Access Control",
                mitigation="Never allow direct use of service role keys. Always go through controlled admin clients with approval gates."
            ))

        # Determine overall risk
        severity_order = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        max_severity = max((severity_order.get(t.severity, 0) for t in threats), default=0)

        overall_risk = "low"
        if max_severity >= 3:
            overall_risk = "critical"
        elif max_severity == 2:
            overall_risk = "high"
        elif max_severity == 1:
            overall_risk = "medium"

        requires_hitl = overall_risk in ["high", "critical"] or any(
            t.category == "Elevation of Privilege" for t in threats
        )

        model = ThreatModel(
            action=action,
            threats=threats,
            overall_risk=overall_risk,
            requires_hitl=requires_hitl
        )

        logger.info(f"Threat model for '{action}': {overall_risk} risk, HITL={requires_hitl}")
        return model

    def generate_threat_report(self, model: ThreatModel) -> str:
        """Generate a human-readable threat report."""
        report = f"\n=== Threat Model Report ===\n"
        report += f"Action: {model.action}\n"
        report += f"Overall Risk: {model.overall_risk.upper()}\n"
        report += f"Requires Human Approval: {model.requires_hitl}\n\n"

        if not model.threats:
            report += "No significant threats identified.\n"
            return report

        for threat in model.threats:
            report += f"[{threat.severity.upper()}] {threat.category}\n"
            report += f"  Description: {threat.description}\n"
            report += f"  Affected: {threat.affected_component}\n"
            report += f"  Mitigation: {threat.mitigation}\n\n"

        return report
