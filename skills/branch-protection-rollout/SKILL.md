---
name: branch-protection-rollout
description: Use when you need to protect the default branch across one or many repos, or when a bad edit reached the default branch because nothing gated it. Applies a solo-founder-safe policy, require a pull request with zero required approvals, require the CI status check to pass, block force-pushes and deletions. Handles main-vs-master automatically and discovers each repo's real CI check name.
metadata:
  version: "1.0.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-04"
---

# Branch Protection Rollout

Solo-founder-safe default-branch protection across repos.

## When to Load
- Protecting main/master across one or many repos
- After a bad edit reached the default branch
- Setting require-PR + CI status + no force-push

## Policy (solo-founder-safe)
- Require pull request (zero required approvals is OK)
- Require CI status check to pass
- Block force-pushes and deletions
- Auto-detect main vs master and real CI check name

## Related Skills
- `release-preflight`
- `build-ci-hygiene`
- `aether-git-workflow`
