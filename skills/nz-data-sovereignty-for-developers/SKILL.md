---
name: nz-data-sovereignty-for-developers
description: Use when a developer, startup, or enterprise team needs practical guidance on implementing Māori data sovereignty (Te Mana Raraunga) and NZ data residency principles in code, architecture, and operations. Handles local-first design, owner-controlled keys, consent patterns, egress controls, and HITL gates for data decisions. Always require Cultural Advisory or founder HITL for any claim of compliance or production deployment involving Māori data.
metadata:
  version: "0.1.0"
  status: design-target
  owner: Coastal Alpine Tech
  last_updated: "2026-07-28"
  tier: sovereignty
  hitl_level: L2+
  cultural_sensitivity: high
---

# NZ Data Sovereignty for Developers

## Purpose

Provide developers, startups, and enterprise teams with concrete, implementable patterns for building systems that respect Te Mana Raraunga principles and New Zealand data residency expectations. This skill turns high-level sovereignty principles into code, architecture, and operational controls.

It is **not** a legal opinion or certification. It is a design-target implementation guide aligned with CAT standards.

## When to Use

- Designing or reviewing systems that process Māori data, community data, or sensitive operational data on whenua.
- Implementing local-first, offline-capable, or edge architectures.
- Adding consent graphs, key ownership, or egress controls.
- Preparing for TPK, iwi, or government conversations that require evidence of data care.
- Auditing existing code for silent exfiltration or cloud-default patterns.

## Core Principles (Te Mana Raraunga mapped to engineering)

| Principle | Engineering translation |
|-----------|-------------------------|
| **Rangatiratanga** | Owner (or authorised collective) controls keys, access policy, and final decisions. |
| **Whakapapa** | Full provenance of data lineage, model versions, and transformations is recorded. |
| **Manaakitanga** | Systems are designed for care — minimise harm, support correction, enable exit. |
| **Kotahitanga** | Collective benefit is considered; individual extraction is avoided. |
| **Kaitiakitanga** | Guardianship — long-term stewardship, no silent deletion or irreversible loss. |

## Mandatory Controls (Minimum Viable Set)

Every system claiming alignment with this skill must implement:

1. **Local-first / offline-capable default**  
   Data is processed and stored on the owner’s infrastructure or edge node by default. Cloud is opt-in and labelled.

2. **Owner-controlled keys**  
   Encryption keys are generated and held under the data owner’s control. Service providers do not hold unrestricted decryption rights.

3. **No silent egress**  
   Any outbound data movement requires explicit, logged consent or policy decision. Fail closed.

4. **Consent / purpose binding**  
   Data use is bound to declared purpose. Secondary use requires new consent or HITL.

5. **HITL on high-impact data decisions**  
   Deletion, bulk export, model training on private data, or sharing with third parties require human approval (L2+).

6. **Audit & provenance**  
   Immutable or append-only logs of access, transformation, and decision events.

7. **Exit / portability path**  
   Owner can extract their data in usable form and revoke access.

## Implementation Patterns (CAT-aligned)

### Edge / Offline Node
- Prefer Raspberry Pi 5 + local LLM (Ollama) + local vector store patterns already used in Kiwi Edge Stack.
- Telemetry stays on-node unless explicitly authorised.
- Use SecurityGuard-style interception for model and data paths.

### Multi-tenant SaaS
- Strong tenant isolation.
- Per-tenant key material where feasible.
- Clear data residency declaration (NZ-preferred).
- No cross-tenant training without explicit consent.

### Cloud components
- Only used when justified.
- Document jurisdiction, sub-processors, and encryption-at-rest / in-transit.
- Prefer NZ or clearly controlled regions.

## HITL Gates (non-negotiable)

- Any production claim of “Te Mana Raraunga aligned” or “sovereign” → Cultural Advisory + founder review.
- Any change that weakens local-first, key ownership, or egress controls → L2 HITL.
- Any grant, LOI, or public statement that references this skill → claim tier check (L1 Designed until runtime evidence).

## Anti-Patterns

- Defaulting all data to a foreign cloud “for convenience”.
- Claiming compliance without enforceable technical controls.
- Training models on customer or Māori data without explicit, purpose-bound consent.
- Treating sovereignty as a marketing badge rather than runtime behaviour.
- Silent telemetry or analytics that leaves the owner’s control.

## Relationship to Existing CAT Skills

- Builds on `te-mana-raraunga-controls` and `aether-data-sovereignty`.
- Complements `aether-nz-ai-safety` and `nz-ai-compliance-soc2`.
- Used by grants-agent and funding narratives when sovereignty evidence is required.
- Must be referenced by any new domain portal or multi-tenant system.

## Success Criteria

A developer using this skill should be able to:

1. Explain the five Te Mana Raraunga principles in engineering terms.
2. Design or review a system against the Minimum Viable Set of controls.
3. Identify and fix silent egress or key-control weaknesses.
4. Produce an architecture note or checklist that can be shown to a Cultural Advisor or funder without over-claiming.

## Version & Status

- Version: 0.1.0
- Status: Design-target (L1)
- Next: Add concrete code patterns and checklists in `references/` after first real usage.
