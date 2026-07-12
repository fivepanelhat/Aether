# Governance — CAT Architectural Standards

This repository is governed by the **Coastal Alpine Tech (CAT) Architectural
Standards** maturity model. The full decision skill lives at
[`skills/cat-architectural-standards/SKILL.md`](./skills/cat-architectural-standards/SKILL.md)
and is bundled with the package so it loads in any Aether session.

## Tier classification

| Tier | Role | Applies to Aether as |
| :--- | :--- | :--- |
| **Platinum** *(primary)* | Intelligent self-improving system | Aether **is** the AI engine — ReAct orchestration, skills, JSONL memory, and the data-flywheel hooks that let the stack learn locally. |
| **Diamond** *(secondary)* | Enterprise-grade foundation | Skills CI, HITL gates, guardrails + threat modeling, least-privilege GitHub Actions, cross-platform (Windows/Linux) hardening. |
| **Gold** *(secondary)* | Workflow-native design | The CLI/remediation/webhook flows mirror a real developer lifecycle end to end. |

## Operating rules

- **Classify before building.** Every non-trivial change declares its primary
  (and any secondary) tier in the PR description or ADR.
- **HITL gates are non-negotiable** (per the standard): any change to
  classification, cultural / Te Mana Raraunga surfaces, security posture, data
  sovereignty, or any release claiming tier compliance requires human approval.
- **Sovereignty overlay applies to all tiers.** Te Tiriti o Waitangi and Te Mana
  Raraunga principles are architectural requirements — local processing, no
  silent cloud exfiltration, cultural review readiness.
- **Load `cat-architectural-standards` first** for any significant planning work;
  it coordinates the other skills (`git-workflow`, `release-preflight`,
  `skill-creator`, `hub-nextjs-component`, …).

## References

- `skills/cat-architectural-standards/SKILL.md` — decision protocol + definitions
- `skills/cat-architectural-standards/references/Skills_to_Tiers_Mapping.md` — skill→tier map
- `SECURITY.md`, `COMPLIANCE.md`, `docs/ARCHITECTURE.md` — Diamond/sovereignty detail
