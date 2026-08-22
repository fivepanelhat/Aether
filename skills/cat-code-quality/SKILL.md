---
name: cat-code-quality
description: Use when setting or reviewing lint, format, typecheck, pre-commit, or PR quality gates for Coastal Alpine Tech Python or TypeScript repos. Defines ruff/format/mypy expectations for the edge stack and eslint/tsc/build for TS hubs. Prevents bulk reformat damage. Trigger phrases include code quality, lint standard, ruff, eslint, pre-commit, quality gate, PR checklist.
metadata:
  version: "0.1.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-22"
  side_effect_class: local-write
  min_hitl_level: L1
  network_posture: none
  resource_envelope: light
  sovereignty_notes: Quality gates only; no secret logging; no silent network
---

# CAT Code Quality

Canonical quality gates for Coastal Alpine Tech product and foundation repos.

## When to use

- Adding or changing lint/format/typecheck CI
- Pre-PR quality checklist
- Aligning a new repo with estate standards
- After a formatting tool is introduced (pair with `cat-lint-safe-edit`)

## Python edge stack (Core, Weaver, stack, portals, harness)

**Preferred toolchain**

| Gate | Tool | Expectation |
|------|------|-------------|
| Lint | `ruff check` | Clean on CI; fix or justify ignores |
| Format | `ruff format` (or project-declared formatter) | Consistent; no mixed tools |
| Types | `mypy` / `pyright` as repo declares | No new errors on touched paths |
| Tests | `pytest` where present | Green on default branch policy |
| Secrets | gitleaks / existing SecOps | No new secrets |

**Rules**

1. Prefer **ruff** over legacy flake8+black pairs when adding new config.
2. Do not introduce a second formatter in the same repo without migration plan.
3. CI should run lint + tests; production apps also need a real **build** step (`build-ci-hygiene`).
4. Lazy env / lazy clients — never parse secrets or construct cloud clients at import time.
5. Workflow YAML must keep valid indentation; never bulk-strip leading whitespace.

## TypeScript / Next hubs (Front_Line_Whanau, CAT-mail, scaffylads)

| Gate | Expectation |
|------|-------------|
| Lint | `eslint` (project config) |
| Types | `tsc --noEmit` or project typecheck script |
| Build | `next build` (or equivalent) in CI with placeholder env |
| Permissions | Workflows declare `permissions:` (default `contents: read`) |

## PR quality checklist (before open)

- [ ] Lint/format clean on changed paths
- [ ] Typecheck clean (or scoped waiver documented)
- [ ] Tests relevant to change pass
- [ ] No secrets, NZBN, IRD, or private keys in diff
- [ ] Workflow YAML still parses if touched
- [ ] Extended PR description written (`cat-pr-ship`)

## Maturity mapping

| Tier | Quality expectation |
|------|---------------------|
| Gold | Lint + tests runnable locally |
| Diamond | CI enforces lint/tests/build; least-privilege Actions; Dependabot |
| Platinum | Quality gates feed flywheel/eval; no auto-merge on red |
| Platinum Edge | Gates runnable on constrained hosts; offline-friendly toolchains |

## Related skills

- `build-ci-hygiene` — CI build + permissions + Dependabot
- `cat-lint-safe-edit` — safe bulk format/encoding
- `repo-recovery-sweep` — recover after a bad sweep
- `ci-failure-triage` — classify red Actions
- `release-preflight` — tag/release sequence
- `cat-pr-ship` — PR description and ship pattern
- `aether-skills-ci` — skills-only validation (not product code)

## HITL

- Changing estate-wide lint defaults across many repos: L2 founder approval
- Single-repo gate tightening: L1 with clear PR description
