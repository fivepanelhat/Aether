---
name: cat-sprint-ai
description: Use when the user says lets do a sprint, CAT Sprint AI, sprint AI, or run a sprint on a CAT surface. Orchestrates scope, review/sweep, prioritised report, execute-by-priority-blocks, prefilled PRs with hyperlinks, and codify-into-skills. Always HITL for production merges and cultural content.
metadata:
  version: "0.1.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-22"
  side_effect_class: local-write
  min_hitl_level: L2
  network_posture: explicit-only
  resource_envelope: light
  sovereignty_notes: No silent exfil; portfolio docs only; founder approves merges
---

# CAT Sprint AI

Operating workflow for hardening, upgrading, and closing gaps across the Coastal Alpine Tech portfolio.

## When to use

- User says: "let's do a sprint", "CAT Sprint AI", "sprint AI", "run a sprint on X"
- Need a structured review → prioritised backlog → block execution → PR ship → skill codify loop

## Sprint loop (mandatory order)

1. **Scope** — confirm surface (repo, layer, governance, skills, runtime). One sentence.
2. **Review / sweep** — load `cat-sprint-report` (or apply its template). Evidence from files/PRs only.
3. **Report** — P0–P3 backlog, strengths, blockers. Wait for user to pick blocks or say go.
4. **Execute by priority blocks** — finish each Pn level before the next unless user reorders.
5. **Ship** — branch `cat/<short-topic>`, lean commit, prefilled PR, return **clickable hyperlinks**.
6. **Codify** — if a pattern repeated twice, draft or update a skill; present for HITL before broad rollout.

## Block format (every execution block)

```text
Block Pn — <name>
Plan: ...
Tools/skills used: ...
Changes: ...
PRs: <markdown hyperlinks>
Status: done | blocked | needs HITL
```

## Ship rules

- Branch naming: `cat/<topic>` (e.g. `cat/register-harness`, `cat/git-hygiene`)
- PR title: conventional, lean (`chore:`, `docs:`, `fix:`)
- PR body: why + what + test plan checklist
- Always return full `https://github.com/fivepanelhat/<repo>/pull/<n>` links
- After user merges: optional status check via GitHub tools; report merged vs still open
- Never force-push to default branch; never merge without explicit user approval unless standing policy exists

## HITL

- L2 default for any write to production branches, cultural content, or external claims
- Skills and docs may be drafted; user confirms before treating as portfolio standard
- Do not invent NZBN, IRD, partner LOIs, or compliance certifications

## Relation to other skills

- `cat-sprint-report` — structured review output
- `cat-architectural-standards` / `cat-architecture-congruence` — maturity and drift
- `aether-hitl-protocol` — gate levels
- `aether-git-workflow` — commit/PR discipline when present
- `aether-skill-authoring` — when codifying new skills from the sprint

## Anti-patterns

- Drive-by refactors outside the agreed scope
- Opening PRs without hyperlinks in the reply
- Skipping the report when user asked for a sprint
- Mixing P0 and P3 in one unfocused commit
- Touching surfaces the founder explicitly excluded
