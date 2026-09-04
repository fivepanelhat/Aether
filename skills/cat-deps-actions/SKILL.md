---
name: cat-deps-actions
description: Use when pinning or upgrading GitHub Actions in CAT workflows. Covers action version pins, permissions blocks, and Dependabot github-actions ecosystem. Trigger phrases include Actions pin, workflow dependencies, actions/checkout version, Dependabot github-actions.
metadata:
  version: "0.1.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-22"
  side_effect_class: local-write
  min_hitl_level: L1
  network_posture: none
  resource_envelope: light
  sovereignty_notes: Workflow changes can break estate CI; validate YAML before push
---

# CAT Deps — GitHub Actions

## When to use

- Bumping actions/checkout, setup-python, setup-node, etc.
- Adding Dependabot for github-actions
- Fixing missing permissions blocks

## Standards

1. Pin actions appropriately for sensitivity of the workflow.
2. Every workflow declares **permissions:** (default contents: read) — see `build-ci-hygiene`.
3. After workflow edits: YAML must parse; prefer green CI on a PR before merge.
4. Do not grant write permissions on PR CI unless required and justified.
5. Bulk action bumps: scoped PRs + `cat-lint-safe-edit` discipline.

## Related

- `cat-deps`, `build-ci-hygiene`, `ci-failure-triage`, `repo-recovery-sweep`, `branch-protection-rollout`
