---
name: cat-deprecation
description: Use when fixing deprecated APIs, packages, language features, or GitHub Actions in CAT repos. Triages deprecation warnings, plans non-breaking then breaking migrations, and prevents silent use of removed APIs. Trigger phrases include deprecated, deprecation warning, fix deprecated, migration off deprecated, outdated API, removed in version.
metadata:
  version: "0.1.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-22"
  side_effect_class: local-write
  min_hitl_level: L1
  network_posture: explicit-only
  resource_envelope: light
  sovereignty_notes: Prefer maintained offline-capable replacements; no drive-by major upgrades without tests
---

# CAT Deprecation

Solve deprecated code and dependency usage without breaking the estate.

## When to use

- CI or local runs show DeprecationWarning or tool deprecated notices
- Package or Action docs mark an API as deprecated
- Planning removal of a legacy path before a major runtime bump
- User says fix deprecated / clean deprecations

## Triage (do this first)

| Signal | Likely class | First move |
|--------|--------------|------------|
| Python DeprecationWarning in our code | Call-site uses old API | Replace call; add test |
| Warning from a dependency | Upstream API change | Bump or wrap; see cat-deps-* |
| ESLint / TypeScript deprecation | TS API or library | Codemod or manual replace |
| Actions deprecated action / runner | Workflow | cat-deps-actions |
| Removed in next major (not yet broken) | Scheduled debt | Issue + milestone |

Label each finding: FACT / INFERENCE / UNKNOWN.

## Resolution order

1. Inventory — path, message, versions, production vs test-only
2. Prefer non-breaking replacement on the same major
3. Isolate shared call sites behind a small adapter if needed
4. Validate — lint + tests (+ build for TS) via cat-code-quality
5. Ship — cat-pr-ship with deprecations cleared in test plan
6. Majors / behaviour change — HITL L2 + matching cat-deps-* skill

## Hard rules

- Do not silence warnings with broad filters unless third-party, unfixable for now, and filter is narrow + commented + ticketed
- Do not upgrade shared Core only to clear a warning without tests green and L2 if major
- Do not mix deprecation cleanup with unrelated refactors in the same PR
- Workflow deprecations: validate YAML; avoid bulk sweeps (cat-lint-safe-edit)

## Related skills

- cat-deps / cat-deps-python / cat-deps-node / cat-deps-actions
- cat-code-quality, cat-pr-ship
- ci-failure-triage, repo-recovery-sweep

## HITL

- L1: local call-site fixes, same-major API replacements
- L2: major runtime/framework upgrades, shared Core API removals, silencing filters on production paths
