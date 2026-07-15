---
name: nz-startup-fleet-bridge
version: "1.0.0"
model_tier: light
type: orchestration
requires_hitl: true
cultural_sensitivity: medium
description: >
  Bridge to NZ Start-Up in a Box founder fleet skills under skills/nz-startup/.
  Load agent-hardening first. Full runtime is the nz-startup CLI in the NZ-Start-Up repo.
metadata:
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-07-15"
tags:
  - nz-startup
  - fleet
  - bridge
---

# NZ Start-Up Fleet Bridge

## When to Use
- Founder OS, EDA white-label, RDTI, GST, grants, board packs, market-fit
- Any request that matches NZ Start-Up digital employees

## Instructions
1. Load `.github/agent-fleet/agent-hardening` and `anti-hallucination.md`.
2. Load skills from `skills/nz-startup/<skill>/SKILL.md`.
3. Prefer running `nz-startup` CLI when available (deterministic tools).
4. Never invent send/file/pay tools or partner deals.

## References
- https://github.com/fivepanelhat/NZ-Start-Up
- `skills/nz-startup/README.md`
