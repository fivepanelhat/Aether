---
name: cat-sprint-report
description: Use during CAT Sprint AI or when the user asks for a review, sweep, or gap report on CAT repos. Produces a prioritised congruence report against Gold Diamond Platinum Platinum Edge, governance, privacy, security, and stack uniformity. Evidence-based only.
metadata:
  version: "0.1.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-22"
  side_effect_class: read-only
  min_hitl_level: L1
  network_posture: explicit-only
  resource_envelope: light
  sovereignty_notes: Read-only report; no data leaving owner control beyond GitHub API used for evidence
---

# CAT Sprint Report

Standard review/sweep report for Coastal Alpine Tech surfaces.

## When to use

- Inside a CAT Sprint AI loop (step 2–3)
- User asks to review, audit, sweep, or gap-check a repo or portfolio layer

## Report template (use this structure)

### 1. Scope
- Repos / paths reviewed
- Standards applied (Gold / Diamond / Platinum / Platinum Edge, HITL, Te Mana Raraunga, privacy, security)

### 2. Strengths
- Bullet list of what already passes (cite files)

### 3. Gaps matrix

| Area | Status | Evidence | Priority |
|------|--------|----------|----------|
| Triad / CAT_CONGRUENCE | | | |
| Stack map uniformity | | | |
| Founding-date hygiene | | | |
| Autonomy / HITL language | | | |
| Privacy / COMPLIANCE | | | |
| Security / threat model | | | |
| Skill / harness contract | | | |
| CI / release discipline | | | |

Status values: **Strong pass** | **Pass** | **Gap** | **Unknown**

### 4. Prioritised backlog

- **P0** — correctness, safety, or broken congruence
- **P1** — uniformity and harness/runtime readiness
- **P2** — hardening and DX
- **P3** — optional estate coverage

### 5. Recommended next block
One clear "do this next" recommendation. Do not start execution until user says go (unless they already ordered a full sprint execute).

## Rules

- Prefer tools and repo files over memory
- Label FACT / INFERENCE / UNKNOWN on non-trivial claims
- Do not invent compliance certificates or partner status
- Keep the report lean enough to act on in one sitting
