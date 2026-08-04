---
name: aether-night-cycle
description: Use when designing, implementing, or running continuous overnight operation for Aether. Handles the Night Cycle (evening summary + prioritised next-day plan) and Morning Brief. Ensures scheduled specialist agents run under hard HITL gates. Trigger phrases include night cycle, overnight loop, morning brief, continuous operation, scheduled agents, policy-based autonomy adapted for sovereignty.
metadata:
  version: "1.0.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-07-16"
  related: aether-core, aether-agent-fleet, aether-hitl-protocol, cat-architectural-standards
---

# Aether Night Cycle

Defines continuous overnight operation for Aether under hard HITL gates. Adapts continuous-agent patterns for sovereign, founder-controlled systems.

## When to Load

- Designing or running the evening summary and next-day plan
- Implementing Morning Brief surfaces
- Scheduling specialist agents overnight
- Reviewing what is allowed to run without real-time human presence

## Core Loop

1. **Evening Summary** — what was completed, what is blocked, what is queued
2. **Prioritised Next-Day Plan** — ordered list of proposed actions with gate levels
3. **Overnight Execution** — only actions covered by standing policy or L0/L1
4. **Morning Brief** — human reviews queue, approves, rejects, or defers

## HITL Rules for Night Cycle

- Overnight proposals default to pending (L2)
- Only standing-policy-covered low-risk actions may execute overnight
- No production deploys, external sends, or cultural content changes overnight without prior explicit approval
- Morning Brief is the primary approval surface

## Related Skills

- `aether-hitl-protocol` for gate levels
- `aether-agent-fleet` for specialist scheduling
- `aether-core` for orchestrator rules
