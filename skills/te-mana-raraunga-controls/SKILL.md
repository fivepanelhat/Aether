---
name: te-mana-raraunga-controls
description: Use when designing, reviewing, implementing, or auditing technical controls that realise Te Mana Raraunga principles in Aether, Coastal Alpine Tech, Whānau Preterm Support Hub, or Mana Kai systems. Provides the concrete Must / Should controls mapped to Rangatiratanga, Whakapapa, Manaakitanga, Kotahitanga and Kaitiakitanga, plus the Minimum Viable Set and runtime sovereignty gate. Always enforce HITL L2+ on sovereignty-affecting changes. Trigger phrases include Te Mana Raraunga controls, sovereignty technical controls, Māori data sovereignty controls, runtime sovereignty gate, consent graph, owner-controlled keys.
metadata:
  version: "0.1.0"
  status: experimental
  owner: Coastal Alpine Tech
  last_updated: "2026-07-27"
  related: aether-data-sovereignty, aether-hitl-protocol, aether-nz-ai-safety, cat-architectural-standards, aether-core
  source: "Te Mana Raraunga principles; Te Kāhui Raraunga Māori Data Governance Model; Aether data-sovereignty and HITL skills; 2025–2026 sovereign infrastructure patterns"
---

# Te Mana Raraunga Technical Controls

Operational catalogue of technical controls that turn Te Mana Raraunga principles into enforceable system behaviour. Complements `aether-data-sovereignty` (principles and non-negotiable rules) by specifying the concrete controls, priorities, and minimum viable set.

## When to Load

- Designing or reviewing any data model, storage, processing, consent, key management, or external model path.
- Implementing or auditing the runtime sovereignty gate or consent graph.
- Architecture Decision Records that claim Te Mana Raraunga alignment.
- Agent or skill work that touches personal, health, cultural, farm, or Māori data.
- Any discussion of “what technical controls actually implement the principles”.

## Priority Legend

- **Must** — Non-negotiable for systems handling Māori, health, or high-sensitivity data.
- **Should** — Strongly expected; any exception requires recorded justification.
- **May** — Recommended when capacity allows.

## 1. Rangatiratanga — Authority & Control

| ID | Control | Priority | Enforcement |
|----|---------|----------|-------------|
| R1 | Documented decision rights for every sensitive data class (owner / kaitiaki + lifecycle rights) | Must | Data model & architecture docs |
| R2 | Prefer Aotearoa-based storage & processing. External location requires recorded justification + approval | Must | Design review + runtime check |
| R3 | Owner- or jointly-controlled encryption keys for high-sensitivity / taonga data | Must | Key management; operators must not hold unilateral decryption |
| R4 | Technical ability to revoke access or trigger cryptographic deletion / key destruction | Must | Linked to consent withdrawal |
| R5 | No silent or permanent transfer of control without explicit owner action | Must | Policy + HITL L2+ |

## 2. Whakapapa — Relationships & Context

| ID | Control | Priority | Enforcement |
|----|---------|----------|-------------|
| W1 | Provenance block on every sensitive record (origin, kaitiaki, collective, timestamp, hash) | Must | Schema-enforced |
| W2 | Maintain and expose meaningful relationships (people, whenua, knowledge, derived artefacts) | Should | Data model + RAG design |
| W3 | Record what was removed or generalised in any transformation / aggregation | Should | Pipeline logging |
| W4 | Lineage for models, embeddings, reports and summaries derived from Māori data | Should | Artefact / model metadata |

## 3. Manaakitanga — Care & Dignity

| ID | Control | Priority | Enforcement |
|----|---------|----------|-------------|
| M1 | High-stakes or public-facing outputs involving Māori data require cultural / ethical review | Must | HITL L2+ + cultural review readiness |
| M2 | Checks (automated + human) for stigmatising or deficit framing | Should | Eval harness + human review |
| M3 | Required medical / funding / cultural disclaimers on relevant outputs | Must | Content generation gates |
| M4 | Prefer processing that minimises identifiability while still meeting purpose | Should | Design principle |

## 4. Kotahitanga — Collective Benefit

| ID | Control | Priority | Enforcement |
|----|---------|----------|-------------|
| K1 | Purpose binding — use limited to consented or authorised purposes | Must | Consent service + access control |
| K2 | Support for collective (iwi / hapū / organisation) consent where appropriate | Should | Consent graph design |
| K3 | Documented benefit / value-sharing arrangement when commercial or research value is created | Should | Governance record |
| K4 | Technical and governance pathway for communities to exit or require changes | Should | Off-boarding + policy |

## 5. Kaitiakitanga — Guardianship

| ID | Control | Priority | Enforcement |
|----|---------|----------|-------------|
| Kt1 | Encryption at rest and in transit for all sensitive classes | Must | Platform baseline |
| Kt2 | Local-first / edge processing preference; only aggregated or consented signals leave the edge | Must | Architecture + runtime preference |
| Kt3 | No silent exfiltration — external model calls and transfers minimised, logged, and gated | Must | Runtime sovereignty gate |
| Kt4 | Audit logs of access, processing and transfer that themselves respect sovereignty rules | Must | Logging design |
| Kt5 | Support for meaningful deletion including cryptographic erasure where appropriate | Must | Lifecycle procedures |
| Kt6 | Sensitivity classification (public / internal / restricted / taonga) with scaled controls | Must | Classification scheme |

## 6. Cross-Cutting Enabling Controls

| ID | Control | Priority | Enforcement |
|----|---------|----------|-------------|
| X1 | Queryable Consent Graph / service — agents must check before personal or cultural data access | Must | Core runtime dependency |
| X2 | Runtime Sovereignty Gate — pre-flight check (consent + residency + sensitivity + approval status) before any off-box or external-model transfer | Must | Fail-closed |
| X3 | Uniform sovereignty metadata block on every sensitive record | Must | Schema + plugin enforcement |
| X4 | HITL binding — all changes to location, keys, consent or external flows gated at L2 or higher | Must | `aether-hitl-protocol` |
| X5 | Fail-closed default — if a required sovereignty check cannot be completed, the action is blocked | Must | System-wide |

## Minimum Viable Set (Early Production)

Implement these first:

1. **X2** Runtime Sovereignty Gate  
2. **X1** Consent check before personal / cultural access  
3. **R2 + Kt2** Local-first / NZ residency preference  
4. **Kt1 + R3** Encryption + owner-influenced key control for high-sensitivity data  
5. **X4** HITL L2+ on all sovereignty-affecting changes  
6. **W1 + X3** Basic provenance + sovereignty metadata  

## HITL & Safety Binding

- Every control that changes data location, key custody, consent status, or external data flows is subject to **HITL L2 or higher**.
- Cost, latency, or convenience ranking is subordinate to these controls.
- Standing policies cannot be used to bypass health, cultural, or irreversible high-impact actions.
- Claims of Te Mana Raraunga alignment require evidence that the relevant Must controls are present and operating.

## Anti-Patterns

- Treating principles as statements of intent without corresponding technical controls.
- Allowing external model calls for sensitive content without a recorded sovereignty gate decision.
- Holding unilateral decryption keys for taonga or high-sensitivity data.
- Logging full personal or cultural content without minimisation and protection.
- Claiming alignment while data routinely leaves Aotearoa without justification and approval.

## Integration

- Load `aether-data-sovereignty` for the principles and non-negotiable rules.
- Load `aether-hitl-protocol` for the gate levels that enforce human authority.
- Load `aether-nz-ai-safety` for fail-closed and Algorithm Charter alignment.
- Apply the Cultural Safety & Sovereignty Overlay from `cat-architectural-standards` to every Gold / Platinum / Diamond decision.
- Use this skill when the question is “what concrete controls implement the principles”.

---

Coastal Alpine Tech · Aether  
te-mana-raraunga-controls v0.1.0 · 27 July 2026
