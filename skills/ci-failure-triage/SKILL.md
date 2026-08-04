---
name: ci-failure-triage
description: Use when a GitHub Actions workflow is showing red, CI is failing, red team is failing, the build is broken, or why is this workflow failing. Distinguishes an invalid-workflow-file parse failure from a real test failure, spots stale red on a pre-fix commit, and knows that schedule-only workflows do not re-run on push so they need a manual dispatch to clear.
metadata:
  version: "1.0.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-04"
---

# CI Failure Triage

Distinguishes invalid-workflow parse failures from real test failures and stale reds.

## When to Load
- CI is red / build is broken
- Need to know if it is YAML parse vs real test failure
- Stale red on a pre-fix commit
- Schedule-only workflows that need manual dispatch

## Triage Steps
1. Is the workflow file itself invalid?
2. Is the failure on the latest commit or stale?
3. Is the workflow schedule-only (needs manual dispatch)?
4. Route real test failures to `ci-failure-parser`

## Related Skills
- `ci-failure-parser`
- `repo-recovery-sweep`
- `notification-responder`
