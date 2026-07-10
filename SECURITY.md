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

- `ThreatModeler` gates high-risk actions to HITL.
- Security skills: route audit, error-message sanitisation, schema enforcement.
- See `examples/security_hardening.py` and `docs/SKILLS_CATALOG.md`.

## Quality gates

- Matrix CI (Python 3.10 / 3.12): ruff, pytest, CLI smoke.
