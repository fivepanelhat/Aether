# Te Mana Raraunga Technical Controls — Audit Checklist

Use this checklist when reviewing a system, skill, or deployment for Te Mana Raraunga technical alignment.

## Minimum Viable Set (must pass for early production)

- [ ] **X2** Runtime Sovereignty Gate exists and is fail-closed
- [ ] **X1** Consent check is performed before personal or cultural data access
- [ ] **R2 + Kt2** Local-first / NZ residency preference is enforced or justified
- [ ] **Kt1 + R3** Encryption at rest/transit + owner-influenced keys for high-sensitivity data
- [ ] **X4** All sovereignty-affecting changes are gated at HITL L2 or higher
- [ ] **W1 + X3** Basic provenance + sovereignty metadata on sensitive records

## Full Catalogue (by principle)

### Rangatiratanga
- [ ] R1 Decision rights documented for every sensitive data class
- [ ] R2 Aotearoa preference + recorded justification for external locations
- [ ] R3 Owner / jointly-controlled keys for high-sensitivity / taonga data
- [ ] R4 Revocation and cryptographic deletion / key destruction supported
- [ ] R5 No silent permanent transfer of control

### Whakapapa
- [ ] W1 Provenance block on sensitive records
- [ ] W2 Meaningful relationships maintained and exposable
- [ ] W3 Transformations record what was removed or generalised
- [ ] W4 Lineage for derived models, embeddings, reports, summaries

### Manaakitanga
- [ ] M1 Cultural / ethical review for high-stakes or public outputs
- [ ] M2 Stigma / deficit framing checks in place
- [ ] M3 Required disclaimers present on relevant outputs
- [ ] M4 Preference for minimising identifiability

### Kotahitanga
- [ ] K1 Purpose binding enforced
- [ ] K2 Collective consent pathways supported where appropriate
- [ ] K3 Benefit / value-sharing arrangements documented when relevant
- [ ] K4 Exit / change pathway exists for communities

### Kaitiakitanga
- [ ] Kt1 Encryption at rest and in transit
- [ ] Kt2 Local-first / edge preference; only consented signals leave edge
- [ ] Kt3 No silent exfiltration; external calls gated and logged
- [ ] Kt4 Sovereignty-respecting audit logs
- [ ] Kt5 Meaningful deletion / cryptographic erasure supported
- [ ] Kt6 Sensitivity classification with scaled controls

### Cross-Cutting
- [ ] X1 Queryable Consent Graph / service
- [ ] X2 Runtime Sovereignty Gate (fail-closed)
- [ ] X3 Uniform sovereignty metadata block
- [ ] X4 HITL L2+ binding on all sovereignty-affecting changes
- [ ] X5 Fail-closed default when checks cannot be completed

## Sign-off

- Reviewer: _______________________
- Date: _______________________
- Evidence location / ADR: _______________________
- Overall status: Pass / Conditional / Fail
