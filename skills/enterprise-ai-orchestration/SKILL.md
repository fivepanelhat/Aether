---
name: enterprise-ai-orchestration
description: Use when designing or reviewing multi-agent systems, multi-tenant platforms, or high-stakes orchestration for enterprise, government, or large organisational contexts. Handles decision rights, escalation ladders, auditability, tenant isolation, HITL ceilings, and governance patterns. Always enforce human authority and NZ AI safety constraints. Trigger phrases include enterprise orchestration, multi-agent governance, high-stakes agents, tenant isolation, orchestration architecture, enterprise AI.
metadata:
  version: "0.1.0"
  status: design-target
  owner: Coastal Alpine Tech
  last_updated: "2026-07-28"
  tier: orchestration
  hitl_level: L2+
  cultural_sensitivity: high
---

# Enterprise AI Orchestration

## Purpose

Provide architecture and governance patterns for running multiple specialised agents and skills safely inside enterprise, government, or large organisational environments. Focus is on decision rights, observability, isolation, and human control rather than maximum autonomy.

## When to Use

- Designing multi-agent fleets for complex workflows.
- Building multi-tenant platforms where different organisations or teams must remain isolated.
- Defining escalation ladders and authority ceilings for high-stakes decisions.
- Preparing architecture for enterprise or public-sector conversations.
- Reviewing existing agent systems for governance gaps.

## Core Principles

1. **Decision rights first**  
   Every significant action has a clear owner (human role or explicit HITL gate). Agents do not invent authority.

2. **Least privilege & isolation**  
   Agents and tenants receive only the tools and data they need. Cross-tenant access is forbidden by default.

3. **Observable by design**  
   Every agent action that affects state, data, or external systems is logged with provenance.

4. **Escalation is a feature**  
   Uncertainty, policy conflict, or high impact triggers escalation rather than silent continuation.

5. **Sovereignty and safety constraints apply at every layer**  
   Local-first preferences, Te Mana Raraunga controls, and NZ AI safety guidelines are inherited by all agents in the fleet.

## Recommended Architecture Patterns

### Orchestrator + Specialist Fleet
- One (or few) orchestrator agents route work to specialised skills/agents.
- Specialists are narrow and versioned.
- Orchestrator holds routing policy and HITL escalation logic.

### Multi-tenant Isolation
- Strong tenant boundaries at data, key, and tool levels.
- No shared model fine-tuning across tenants without explicit consent.
- Clear residency and processing declarations per tenant.

### Escalation Ladder (example)
1. Agent attempts task within policy.
2. Soft uncertainty → request clarification or additional context.
3. Policy or high-impact boundary → escalate to human reviewer (L2).
4. Cultural, legal, or sovereignty impact → Cultural Advisory / founder (L3).

## HITL & Governance Requirements

- Production orchestration changes require L2 HITL.
- Any pathway that can affect customer data, Māori data, grants, or external communications requires elevated gates.
- Audit logs must be retained and accessible to authorised humans.
- Claim language remains Design-target until runtime evidence and scorecards support higher tiers.

## Relationship to Existing Skills

- Builds on `aether-agent-fleet`, `aether-hitl-protocol`, `aether-whanau-hub-architecture`, Weaver patterns.
- Inherits constraints from `nz-data-sovereignty-for-developers`, `aether-nz-ai-safety`, and `te-mana-raraunga-controls`.
- Uses evaluation and performance skills for continuous improvement.

## Anti-Patterns

- Single monolithic agent that “does everything”.
- Agents that can grant themselves new tools or escalate their own privileges.
- Shared global memory across tenants without isolation.
- Hidden decision logic that cannot be audited.
- Claiming “enterprise-ready” without measured isolation, logging, and HITL evidence.

## Success Criteria

A team using this skill should be able to:

1. Define clear decision rights and escalation paths for a multi-agent system.
2. Design tenant isolation that prevents cross-contamination.
3. Produce an architecture note that can be shown to enterprise or public-sector stakeholders without over-claiming.
4. Identify and close governance gaps in existing agent fleets.
5. Maintain Design-target language until runtime evidence exists.

## Version & Status

- Version: 0.1.0
- Status: Design-target (L1)
- Next: Add concrete escalation templates and multi-tenant checklist after first real design usage.
