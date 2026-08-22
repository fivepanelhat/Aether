---
name: cat-deps
description: Meta skill for Coastal Alpine Tech dependency policy. Use when deciding how to audit, pin, upgrade, or Dependabot-cover Python, Node, or GitHub Actions deps across the estate. Routes to cat-deps-python, cat-deps-node, cat-deps-actions. Trigger phrases include dependencies, Dependabot, dep policy, upgrade policy, dependency family.
metadata:
  version: "0.1.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-22"
  side_effect_class: read-only
  min_hitl_level: L1
  network_posture: explicit-only
  resource_envelope: light
  sovereignty_notes: Policy only; upgrades that change production behaviour need L2
---

# CAT Deps (meta)

Orchestrates dependency hygiene for the Kiwi Edge estate.

## When to use

- "What is our dep policy?"
- Planning Dependabot or audit coverage
- Choosing which specialist skill to load for a repo
- Before multi-repo version bumps

## Family map

| Skill | Surface |
|-------|--------|
| `cat-deps-python` | pip / uv / pyproject / requirements, pip-audit |
| `cat-deps-node` | npm / pnpm, package-lock, npm audit |
| `cat-deps-actions` | GitHub Actions action pins, workflow perms |
| `secops-ci-estate-scan` | Estate-wide audit report (read-only) |
| `build-ci-hygiene` | Dependabot present + least-privilege CI |
| `release-preflight` | Before publishing tags with new deps |

## Estate policy (defaults)

1. **Pin for reproducibility** — lockfiles committed where the ecosystem expects them.
2. **Dependabot on by default** for `pip`, `npm`, and `github-actions` ecosystems present in the repo.
3. **Prefer minor/patch auto-PRs**; **major bumps are HITL L2** with changelog skim.
4. **No silent major upgrades** on Core / Weaver / portals without tests green.
5. **Security advisories** — critical/high: triage within sprint cadence; do not ignore GHSA without written deferral.
6. **Local-first** — avoid new runtime deps that force cloud phone-home without explicit justification.

## Routing

```text
Python edge repo     → cat-deps-python
TS / Next hub        → cat-deps-node
Workflow-only change → cat-deps-actions
Whole-org scan       → secops-ci-estate-scan
PR ship              → cat-pr-ship + cat-code-quality
```

## Maturity

| Tier | Dep expectation |
|------|-----------------|
| Gold | Lockfiles or pins; known install path |
| Diamond | Dependabot + CI install from lockfile; Actions pinned |
| Platinum | Audit in SecOps cadence; majors gated |
| Platinum Edge | Lean dep trees; edge images stay small |

## HITL

- Major version bumps across shared Core: L2
- Adding a dependency with network side effects: L2 + sovereignty note
