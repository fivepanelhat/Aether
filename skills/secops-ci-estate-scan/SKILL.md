---
name: secops-ci-estate-scan
description: Use when you want a security and CI health sweep across all your repos, run a secops scan, red team scan, audit my repos for security, check CI across everything, or before a fundraise/partnership. Clones each repo and runs Bandit SAST, dependency audits, a secret scan, workflow YAML validation, and a live deploy health check, then writes a prioritized findings report. Read-only and non-destructive.
metadata:
  version: "1.0.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-04"
---

# SecOps CI Estate Scan

Read-only security and CI health sweep across repos.

## When to Load
- Estate-wide secops / red-team style scan
- Before fundraise or partnership
- CI health check across everything

## Scope (read-only)
- Bandit SAST
- Dependency audits
- Secret scan
- Workflow YAML validation
- Live deploy health check
- Prioritised findings report

## Non-Negotiables
- Non-destructive by default
- HITL before any blocking or quarantine action

## Related Skills
- `ci-failure-parser`
- `release-preflight`
- `aether-hitl-protocol`
