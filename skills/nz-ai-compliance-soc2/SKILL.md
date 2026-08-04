---
name: nz-ai-compliance-soc2
description: New Zealand AI Compliance + SOC 2 Type II framework for Coastal Alpine Tech stack. Enforces Privacy Act 2020 (IPPs), Te Mana Raraunga data sovereignty, MBIE Responsible AI, Algorithm Charter for Aotearoa, and SOC 2 Type II controls (audit logging, access controls, data retention, breach detection). Mandatory for all Weaver, Core, Stack, and Aether production deployments.
metadata:
  version: "1.0.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-07-12"
  type: compliance-governance
  requires_hitl: true
---

# NZ AI Compliance + SOC 2 Type II Framework

Operational compliance framework for CAT production systems. Combines Privacy Act 2020, Te Mana Raraunga, MBIE Responsible AI, Algorithm Charter, and SOC 2 Type II control themes.

## When to Load

- Designing or reviewing production deployments (Weaver, Core, Stack, Aether)
- Preparing compliance evidence for partners, funders, or audits
- Mapping controls to Privacy Act IPPs and SOC 2 trust service criteria
- Breach detection, access control, or retention design

## Control Themes

1. **Privacy Act 2020 / IPPs** — purpose, collection, storage, access, correction, retention, disclosure
2. **Te Mana Raraunga** — rangatiratanga, local custody, consent, no silent exfil
3. **MBIE Responsible AI + Algorithm Charter** — transparency, human oversight, fairness, contestability
4. **SOC 2 Type II themes** — security, availability, processing integrity, confidentiality, privacy (evidence over time)

## Mandatory for Production

- Audit logging of sensitive actions
- Access controls and least privilege
- Data retention and deletion pathways
- Breach detection and response outline
- HITL for high-impact automated decisions

## Related Skills

- `aether-nz-ai-safety`
- `te-mana-raraunga-controls`
- `aether-data-sovereignty`
- `aether-hitl-protocol`
