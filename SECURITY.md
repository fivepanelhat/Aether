# Security Policy — Aether

Sovereign agentic development orchestrator (skills, HITL, threat modeling).

## Supported Versions

| Branch | Supported |
| ------ | --------- |
| `main` | Yes |

## Vulnerability Disclosure

Report privately via GitHub Security Advisory or maintainers. Do not file public exploit details.

## Security Notifications

| Channel | Response |
| ------- | -------- |
| Dependabot (pip + Actions) | Weekly; prioritise security labels |
| Code scanning | Enable/triage when analysis available |
| Skills catalog | Security route audit, error sanitisation, strict schema skills |
| Transitive deps | Floor vulnerable packages when pulled via optional stacks |

## Active patches (2026-07)

| ID | Note |
| -- | ---- |
| GHSA-f4xh-w4cj-qxq8 (`langsmith`) | Transitive risk when LangChain stack is installed — require `>=0.8.18` |
| GHSA-4xgf-cpjx-pc3j (`pydantic-settings`) | Require `>=2.14.2` when settings sources are used |
| Workflow permissions | CI sets `permissions: contents: read` |

## Built-in controls

- `ThreatModeler` + `Guardrails` gate high-risk **tools** to HITL.
- **Skill frontmatter** `requires_hitl: true` or `cultural_sensitivity: high` also requires HITL before the skill playbook is applied.
- GitHub webhooks are **propose-only** by default (`auto_remediate=False`). Set `AETHER_WEBHOOK_AUTO_REMEDIATE=1` only when unattended writes are intentional.
- Security skills: route audit, error-message sanitisation, schema enforcement, notifications triage, Te Mana Raraunga sovereignty.
- See `examples/security_hardening.py` and `docs/SKILLS_CATALOG.md`.

## Quality gates

- Matrix CI (Python 3.10 / 3.12): ruff, pytest, CLI smoke.

## Fleet security principles

- **No silent exfiltration** of personal or tenant operational data
- Prefer **local-first** processing; third-party AI only with explicit operator configuration and UI/docs disclosure
- Report vulnerabilities via GitHub Security Advisories or the maintainer contact on the org profile
- High-stakes production changes require human approval (HITL)

## Data sales and third parties

- **We do not sell personal information or customer operational data to third parties.**
- Optional AI or cloud services run only when configured by the operator; processing must be disclosed (in-product and/or docs).
- Prefer local-first paths so third-party transfer is unnecessary by default.

## NZ Privacy Act and Te Mana Raraunga

- Design in accordance with the **Privacy Act 2020**.
- Operate in accordance with **Te Mana Raraunga** principles for Māori data sovereignty interests.
- Align AI features with **NZ AI safety** / responsible AI expectations (HITL, transparency, no silent training on private content).

