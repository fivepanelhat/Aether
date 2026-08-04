---
name: repo-recovery-sweep
description: Use when a bulk edit (a formatting, encoding, ASCII-safe, mojibake, or lint sweep) has broken code or CI across one or more repos. Symptoms include Invalid workflow file, IndentationError, collapsed indentation, packages that will not install, or every Actions run failing at parse. Reverts the offending merge safely and validates (Python compile plus workflow YAML parse) BEFORE any push.
metadata:
  version: "1.0.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-04"
---

# Repo Recovery Sweep

Recover from bulk-edit damage across repos. Validate before push.

## When to Load
- Invalid workflow file / YAML parse failures after a sweep
- IndentationError or collapsed indentation
- Packages will not install
- Every Actions run failing at parse

## Protocol
1. Identify the offending merge/commit
2. Revert safely
3. Validate (Python compile + workflow YAML parse)
4. Only then push — always human approval for the push

## Related Skills
- `ci-failure-parser`
- `ci-failure-triage`
- `branch-protection-rollout`
