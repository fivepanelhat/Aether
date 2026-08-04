---
name: aether-hitl-protocol
description: Use when designing, implementing, or reviewing Human-in-the-Loop gates for Aether. Defines gate levels, escalation triggers, approval artefacts, audit requirements, and standing-policy patterns. Always enforce explicit user approval for production code, health information, cultural content, external actions, or deployments. Trigger phrases include HITL, human in the loop, approval gate, escalation, standing policy, require approval.
metadata:
  version: "1.0.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-07-16"
  related: aether-core, aether-agent-fleet, aether-night-cycle, aether-whanau-hub-architecture, cat-architectural-standards
---

# Aether HITL Protocol

Defines the concrete, reusable Human-in-the-Loop patterns that keep Aether sovereign, safe, and trustworthy. This skill expands the high-level HITL rules in `aether-core` into operational gate levels and implementation guidance.

## When to Load

- Designing or reviewing any agent action that can affect production code, health data, cultural content, external systems, or deployments.
- Implementing approval gates, escalation ladders, or standing policies.
- Auditing whether a workflow has adequate human authority ceilings.
- Any discussion of HITL levels, approval artefacts, or fail-closed behaviour.

## Gate Levels (summary)

| Level | Name | When required |
|-------|------|---------------|
| L0 | Informational | Low-risk, reversible, no external effect |
| L1 | Soft gate | Drafts, suggestions, internal artefacts |
| L2 | Explicit approval | Production code, data location/key changes, cultural content, external sends |
| L3 | Dual / elevated | High-stakes sovereignty, health, financial, or legal actions |

Always escalate to at least L2 for production code, health information, cultural content, external actions, or deployments.

## Core Rules

1. Agents inform, draft, prepare, monitor, and remind. Humans advise, sign, file, send, and pay.
2. No silent side-effects. Any action that leaves the local boundary or changes production state requires an explicit human gate.
3. Approval artefacts must be durable and auditable (who, what, when, scope).
4. Standing policies can pre-authorise narrow, low-risk classes of action; they do not replace L2+ for high-stakes work.
5. Fail closed when consent, residency, or sensitivity checks are missing or ambiguous.

## Integration

- Load with `aether-core` for the primary orchestrator protocol.
- Pair with `aether-data-sovereignty` and `te-mana-raraunga-controls` when data or cultural content is involved.
- Pair with `aether-agent-fleet` when defining agent actions.
- Pair with `aether-night-cycle` when the gate participates in continuous operation.
- Pair with `aether-whanau-hub-architecture` for Hub-specific sensitivity.
