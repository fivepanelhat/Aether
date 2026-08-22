---
name: cat-pr-ship
description: Use when opening, describing, or checking Coastal Alpine Tech pull requests. Enforces branch naming, full extended PR description (why/what/claims/test plan/follow-ups), clickable hyperlinks, and merge hygiene. Trigger phrases include open PR, PR description, ship PR, extended description, merge hygiene.
metadata:
  version: "0.1.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-22"
  side_effect_class: local-write
  min_hitl_level: L2
  network_posture: explicit-only
  resource_envelope: light
  sovereignty_notes: No force-push to default; founder approves merges unless standing policy
---

# CAT PR Ship

Ship pattern for Coastal Alpine Tech PRs.

## When to use

- Opening any PR from a sprint or agent-assisted change
- User asks for PR hyperlinks or merge status
- Codifying the standing rule: **always fill the extended description box**

## Branch naming

`cat/<short-topic>`  
Examples: `cat/register-harness`, `cat/l1-partner-language`, `cat/code-quality-skills`

## Extended PR description (required)

```markdown
## Why
<problem or congruence gap>

## What changed
- <files / behaviour>

## Claim / HITL notes
- Claim tier if external language touched (e.g. L1 Designed)
- HITL implications if any

## Test plan
- [ ] ...
- [ ] ...

## Follow-ups
- <optional next steps>
```

## Reply to founder

Always return **full clickable** links:

`https://github.com/fivepanelhat/<repo>/pull/<n>`

## Merge hygiene

- Do not merge without explicit founder approval (unless standing policy)
- Do not force-push to `main` / `master`
- After merge, optional status check: merged vs still open
- Prefer delete feature branch after merge when safe

## Related

- `cat-sprint-ai` — sprint loop that calls this at ship step
- `cat-code-quality` — quality checklist before open
- `aether-git-workflow` — deeper git discipline when loaded
- `release-preflight` — before tags/releases

## HITL

L2 for production branch merges and any PR that changes cultural, health, or compliance claims.
