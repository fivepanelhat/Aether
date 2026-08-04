---
name: cat-architecture-congruence
description: Use when starting any new Coastal Alpine Tech product, repo, or major feature, or when an agent (including Grok Build) has drifted from the intended architecture. Enforces the mandatory ARCHITECTURE.md + AGENTS.md + CAT_CONGRUENCE.md triad, local-first progressive enhancement, Hybrid Intelligent Layer pattern, and Agent Drift Recovery protocol. Always require HITL before accepting architectural changes.
metadata:
  version: "1.0.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-07-20"
---

# CAT Architecture Congruence

Enforces the mandatory documentation triad and recovery protocol so every CAT product stays aligned with the intended architecture.

## When to Load

- Starting a new product, repo, or major feature
- Suspecting agent or human drift from the architecture
- Reviewing whether ARCHITECTURE.md, AGENTS.md, and CAT_CONGRUENCE.md are present and current
- Applying Agent Drift Recovery

## The Triad (mandatory)

1. **ARCHITECTURE.md** — system shape, boundaries, data flow, edge vs hub
2. **AGENTS.md** — agent roles, tools, HITL expectations
3. **CAT_CONGRUENCE.md** — how this repo maps to Gold/Platinum/Diamond and Te Mana Raraunga

## Hybrid Intelligent Layer

Local-first progressive enhancement: edge inference and local state first; cloud only when consented and gated.

## Agent Drift Recovery

1. Detect drift (missing triad files, contradictory behaviour, unapproved external calls)
2. Pause high-impact actions
3. Re-read triad + aether-core + relevant skills
4. Propose realignment under HITL L2+
5. Do not accept architectural change without explicit founder approval

## Related Skills

- `cat-architectural-standards`
- `aether-core`
- `aether-hitl-protocol`
