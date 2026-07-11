---
name: security-notifications-triage
description: Triages and patches GitHub security notifications across the Kiwi Edge estate — Dependabot/GHSA, CodeQL (workflow permissions, clear-text secrets), pip-audit/npm audit floors, SECURITY.md threat registers.
version: "1.0.0"
type: security
requires_hitl: true
cultural_sensitivity: medium
tags: [security, dependabot, codeql, ghsa, secops, supply-chain]
---

# Security Notifications Triage

## Overview
Operational skill for the **2026-07 org security pass**: turn Dependabot, Code scanning, and advisory findings into code + docs + dep floors without weakening multi-tenant or actuator safety.

## When to Use
- User asks to act on security notifications, alerts, or GHSA/CVE lists
- Open CodeQL findings (`actions/missing-workflow-permissions`, clear-text storage, etc.)
- `pip-audit` / `npm audit` report vulnerable floors
- Updating SECURITY.md / posture reports after a patch sprint

## Instructions

### 1. Collect notifications
For each relevant repo:
- Dependabot open alerts
- Code scanning open alerts
- Secret scanning (if enabled)
- Local `pip-audit -r requirements.txt` / `npm audit`

### 2. Prioritise
| Severity | Examples | Target |
| -------- | -------- | ------ |
| Critical | Pre-auth RCE, secret leak | Mitigate ≤48h |
| High | Arbitrary file read, auth bypass | ≤5 business days |
| Medium | Symlink escape, missing workflow perms | Next patch train |
| Residual no-fix | e.g. chromadb GHSA-f4j7 | Document localhost-only + NetworkPolicy |

### 3. Patch patterns (estate standards)
1. **GITHUB_TOKEN** — top-level `permissions: contents: read` on CI; release jobs may use `contents: write` only
2. **Secrets on disk** — never write API keys from tools; env / operator-managed `.env` (gitignored)
3. **Dep floors** — e.g. `langsmith>=0.8.18`, `pydantic-settings>=2.14.2`
4. **Dependabot** — weekly `pip`/`npm`/`github-actions` (and docker where relevant)
5. **SecurityGuard** — expand patterns in Core; re-run Core tests
6. **Docs** — SECURITY.md threat register + SECURITY_POSTURE_REPORT date stamp

### 4. Verify & ship
- Lint/tests green on touched packages
- Conventional commit `security: …`
- Push member repos first; bump monorepo submodules when Core/portals move

## Guardrails & Constraints
- `requires_hitl: true` for production secret rotation and any force-push / tag rewrite
- Do not dismiss Critical advisories without written mitigation
- Do not weaken actuator guards to silence scanners
- Prefer fix-forward on `main` over long-lived security branches for edge nodes

## Input / Output
- **In:** repo list, alert dumps, audit output
- **Out:** patched files, updated SECURITY.md, commit SHAs, residual risk notes

## References
- `kiwi-edge-architecture`
- Core `SECURITY.md`, stack `SECURITY_POSTURE_REPORT.md`
- Related: `release-preflight`, `build-ci-hygiene`, `error-message-sanitization`
