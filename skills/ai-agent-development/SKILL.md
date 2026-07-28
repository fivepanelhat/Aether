---
name: ai-agent-development
description: Use when designing, scaffolding, implementing, or hardening AI agents and multi-agent systems for production use. Handles agent architecture patterns, tool schemas, memory, HITL gates, evaluation, and progressive disclosure. Always enforce human authority ceilings and NZ AI safety constraints. Trigger phrases include create agent, agent design, multi-agent system, agent scaffolding, production agent, agent hardening.
metadata:
  version: "0.1.0"
  status: design-target
  owner: Coastal Alpine Tech
  last_updated: "2026-07-28"
  tier: agent-development
  hitl_level: L2 on production paths
  cultural_sensitivity: medium
---

# AI Agent Development

## Purpose

Provide a consistent, production-oriented path for creating reliable AI agents and multi-agent systems under Coastal Alpine Tech standards. This skill turns general agent knowledge into CAT-specific architecture, safety, and delivery patterns.

It is a design-target skill. Runtime evidence is required before any “production-proven” claims.

## When to Use

- Designing a new specialist agent or agent fleet.
- Scaffolding an agent with tools, memory, and evaluation.
- Hardening an existing agent for production or high-stakes use.
- Defining HITL gates and decision rights for agentic workflows.
- Reviewing agent architectures against NZ AI safety and Te Mana Raraunga expectations.

## Core Design Principles (CAT)

1. **Human authority is non-negotiable**  
   Agents draft, recommend, and prepare. Humans decide on high-stakes, cultural, legal, or external actions.

2. **Progressive disclosure**  
   Start with minimal context. Load skills and references only when needed. Prefer small, focused skills over monolithic agents.

3. **Observable & evaluable**  
   Every agent must have clear success criteria and a path to measurement (see aether-eval-harness / aether-agent-performance).

4. **Fail closed**  
   When uncertain, when tools fail, or when policy is unclear, the agent stops and escalates rather than guessing.

5. **Sovereignty by default**  
   Local-first processing, owner-controlled data paths, and no silent exfiltration (cross-reference `nz-data-sovereignty-for-developers`).

## Standard Agent Structure

```
agent-name/
├── SKILL.md                 # or agent definition
├── tools/                   # tool schemas and implementations
├── memory/                  # short / long-term patterns
├── evaluation/              # test cases and success criteria
└── references/              # deeper guidance
```

## Development Sequence

1. **Define purpose and boundaries**  
   What is in scope? What is explicitly out of scope? What decisions require human approval?

2. **Identify required tools and skills**  
   Prefer existing skills. Create new ones only when a clear gap exists.

3. **Design HITL gates**  
   Map every high-impact action to an explicit approval level (L1 advisory → L2 required → L3 cultural/founder).

4. **Scaffold with progressive disclosure**  
   Keep the primary instruction set short. Move detailed knowledge into loadable references.

5. **Add evaluation harness**  
   Define 3–5 realistic test cases. Include both happy-path and failure/edge cases.

6. **Harden**  
   Apply agent-hardening patterns (refusal calibration, path sandboxing, secret refusal, watermarking where appropriate).

7. **Document claim tier**  
   Mark as Design-target until runtime evidence exists.

## HITL Requirements

- Any agent that can affect production code, customer data, cultural content, grants, or external communications requires L2 HITL on those paths.
- Agents must never auto-commit, auto-send, or auto-submit without explicit human approval.
- Cultural content or Māori data pathways require Cultural Advisory readiness.

## Anti-Patterns

- Building unconstrained “do anything” agents.
- Hiding decision logic inside long system prompts with no evaluation.
- Claiming production readiness without measured success criteria.
- Skipping HITL because “the model is smart enough”.
- Creating agents that silently call external services or exfiltrate data.

## Relationship to Existing Skills

- Builds on `aether-core`, `aether-agent-fleet`, `agent-hardening`, `aether-hitl-protocol`.
- Uses `aether-eval-harness` and `aether-agent-performance` for measurement.
- Must respect `nz-data-sovereignty-for-developers` and `aether-nz-ai-safety`.
- New specialist agents should be registered under the Aether fleet patterns.

## Success Criteria

A developer using this skill should be able to:

1. Produce a clear agent purpose statement and boundary list.
2. Scaffold a minimal viable agent with tools and HITL gates.
3. Define evaluable success criteria.
4. Identify and remove unconstrained or high-risk behaviours.
5. Document the agent at Design-target tier with a path to higher maturity.

## Version & Status

- Version: 0.1.0
- Status: Design-target (L1)
- Next: Add concrete templates and evaluation examples after first real usage.
