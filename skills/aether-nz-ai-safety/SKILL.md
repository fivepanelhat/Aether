---
name: aether-nz-ai-safety
description: Use when hardening, reviewing, implementing, or auditing AI safety guidelines for Coastal Alpine Tech, Aether, Kiwi Edge Stack, or any NZ-context sovereign edge or agentic system. Applies official NZ frameworks (Public Service AI Framework, MBIE Responsible AI Guidance, Algorithm Charter) plus Te Mana Raraunga, HITL, and fail-closed controls. Trigger phrases include harden nz ai safety, AI safety guidelines, Algorithm Charter alignment, Public Service AI Framework, NZ AI policy, safety hardening, risk tiering.
metadata:
  version: "1.0.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-07-16"
  related: aether-core, aether-hitl-protocol, aether-data-sovereignty, cat-architectural-standards, aether-whanau-hub-architecture
---

# Aether NZ AI Safety (Hardened)

Hardened operational AI safety guidelines for sovereign edge, hybrid agentic, and offline-first systems developed under Coastal Alpine Tech. These guidelines take current New Zealand official materials and make them enforceable, fail-closed, and production-ready for pre-seed to pilot stage.

They sit above `aether-hitl-protocol` and `aether-data-sovereignty` and must be applied together with them.

## When to Load This Skill

- Creating or updating AI safety policy, guidelines, or guardrails.
- Reviewing a new agent, portal feature, model path, or data flywheel for safety.
- Preparing pilots, LOIs, grant applications, or investor materials that claim responsible AI.
- Aligning with Public Service AI Framework, Algorithm Charter, or MBIE Responsible AI Guidance.
- Any discussion of risk tiers, cultural safety for AI, or Te Tiriti + AI.

## Core Hardened Principles

1. **Human Authority is Non-Negotiable**  
   Agents may only inform, draft, prepare, monitor, and remind. Humans alone advise, decide, sign, file, send, pay, or actuate high-impact controls. No system may present agent output as final authority.

2. **Sovereignty First**  
   Prefer local / on-device / NZ-resident processing. Owner-controlled keys. No silent exfiltration. Explicit consent graphs. Treat Māori data and knowledge as taonga under rangatiratanga (see `aether-data-sovereignty`).

3. **Fail-Closed & Least Privilege**  
   Default deny. SecurityGuard-style screening, injection defence, tenant isolation, and capability gating are mandatory. Systems must degrade to safe deterministic behaviour when models or connectivity fail.

4. **Transparency with Purpose**  
   Maintain structured, auditable trails of prompts, decisions, tool calls, and human overrides. Explanations must be meaningful to the affected party and to cultural advisors where relevant. Align with Algorithm Charter transparency commitments.

5. **Cultural Safety & Te Tiriti Partnership**  
   Actively mitigate cultural bias (especially mātauranga Māori, te reo, Pacific knowledge). Embed Te Ao Māori perspectives in design and evaluation. Partnership is operational.

6. **Risk-Proportionate Oversight**  
   Risk tier determines required HITL level, review frequency, and approval authority. High-impact or novel uses require elevated review.

7. **Continuous Assurance**  
   Grounding, verification, red-teaming, and outcome recording are required. Ungrounded high-stakes content is a safety failure.

8. **Accountability**  
   Clear ownership, versioned policies, and retained records sufficient for regulatory, cultural, or legal scrutiny.

## Alignment with Official NZ Frameworks

- **Public Service AI Framework** (GCDO) — OECD-derived principles + Te Tiriti considerations.
- **Responsible AI Guidance for the Public Service: GenAI** and MBIE business guidance.
- **Algorithm Charter for Aotearoa New Zealand** — Transparency, partnership, human oversight, impact assessment.
- **Privacy Act 2020**, sector legislation, and NCSC cyber posture.
- **Te Mana Raraunga** principles (Rangatiratanga, Whakapapa, Manaakitanga, Kaitiakitanga, Kotahitanga).

These guidelines exceed the voluntary nature of the business guidance by making key controls mandatory for CAT systems.

## Risk Tiering & HITL Mapping

Use the standard gate levels from `aether-hitl-protocol` (L0–L4). Map risk as follows:

| Tier     | Examples                                      | Minimum Gate | Additional Requirements                  |
|----------|-----------------------------------------------|--------------|------------------------------------------|
| Low      | Internal drafting, non-personal research      | L0 / L1     | Logging + basic SecurityGuard            |
| Medium   | Tenant-facing advice, operational recommendations | L2       | Explicit approval before action          |
| High     | Actuation, safety-critical decisions, personal/Māori data, regulatory compliance, computer-use on production | L2 or L3 | Multi-person or elevated review + cultural check where relevant + full audit |
| Critical / Novel | New model classes, cross-border data, high-stakes autonomous loops, public high-impact systems | L3 or L4 | Formal impact assessment + external/cultural advisory input + founder-level gate |

Default for any new external, production, health, cultural, or deployment action is **L2**.

## Mandatory Technical Controls

- Every agent and portal path must run SecurityGuard (or equivalent) before model invocation and before external action.
- Hard HITL stops for write actions, computer-use actuation, high-impact recommendations, data export, and model updates.
- Local-first preference (Ollama / edge models). Cloud models only with explicit justification, data minimisation, and documented flow.
- Strict tenant and data isolation.
- Structured logging with human-readable audit views.
- Adversarial testing (prompt injection, cultural bias, capability escalation) before promotion.
- Explicit purpose limitation and consent checks for personal or cultural data.

## Implementation Checklist

When hardening or reviewing a system:

1. Confirm risk tier and required HITL level.
2. Verify SecurityGuard (or equivalent) is on every model path.
3. Confirm local-first or justified external model use with data minimisation.
4. Check consent graph / purpose limitation for any personal or Māori data.
5. Ensure audit trail captures prompts, decisions, tool calls, and overrides.
6. Confirm cultural safety review path exists for High/Critical items.
7. Document residual risks and owner.
8. Update the system register if this is a new production or pilot system.

## Anti-Patterns

- Treating voluntary NZ business guidance as sufficient without hardening.
- Claiming Te Mana Raraunga or Algorithm Charter alignment without concrete controls.
- Allowing agent outputs to be treated as authoritative without human gate.
- Defaulting to cloud models for convenience on sensitive workloads.
- Skipping impact assessment for High/Critical or novel uses.
- Logging full prompts containing personal or cultural data without minimisation.

## Related Skills & Artefacts

- `aether-hitl-protocol` — concrete gate levels and approval artefacts.
- `aether-data-sovereignty` — Te Mana Raraunga operational rules.
- `aether-core` — overall orchestrator principles.
- `cat-architectural-standards` — maturity tiers (Gold / Platinum / Diamond).

For the full standalone policy document suitable for repo root or external sharing, see the companion artefact in the project artifacts or references.

## HITL for This Skill

Any change to these guidelines themselves, or any claim of compliance in external materials (grants, investor decks, public statements), requires explicit user approval (L2+).
