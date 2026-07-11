---
name: te-mana-raraunga-sovereignty
description: Enforces Te Mana Raraunga 2018 (Māori data sovereignty) principles when changing Kiwi Edge stack, portals, firmware, Core, or Aether — local processing, whenua custody, no silent cloud exfil.
version: "1.0.0"
type: security
requires_hitl: true
cultural_sensitivity: high
tags: [te-mana-raraunga, data-sovereignty, aotearoa, kaitiakitanga, compliance]
---

# Te Mana Raraunga Sovereignty

## Overview
Applies **Te Mana Raraunga 2018** (Māori Data Sovereignty Network principles) as an architectural constraint across the Kiwi Edge AI Stack and companion tools. Portfolio rows for Core, coastal-alpine-stack, Sovereign-Edge-Firmware, and Aether list this as their Core NZ regulation baseline.

## When to Use
- Designing or reviewing data flows, storage, telemetry export, or multi-tenant RAG
- Updating portfolio / compliance / architecture docs
- Adding cloud services, analytics, or third-party model APIs
- Working on whenua-linked domains (soil, water, biosecurity, whānau platforms)

## Instructions

### 1. Check custody
- Where is data created? (farm, catchment, hive, clinic, edge node)
- Who holds keys and retention decisions?
- Does any path leave Aotearoa or the operator-controlled premises by default?

### 2. Prefer sovereign defaults
- Inference: Ollama / Hailo on-device
- Bus: mTLS MQTT on-site, not public brokers with shared tenants
- Stores: local SQLCipher / Chroma localhost / flywheel JSONL on node
- CI secrets: never commit `.env`, PEM, or service role keys

### 3. Document alignment
When touching landing portfolio or SECURITY/COMPLIANCE docs:
- Core NZ Regulations for Core / stack / firmware / Aether → **Te Mana Raraunga 2018**
- Domain portals keep their sector Acts **and** remain Te Mana Raraunga–aligned via offline edge design

### 4. Escalate HITL
Require human approval when proposing:
- Off-site model hosting or training uploads
- Cross-tenant data mixing
- Public analytics SDKs on sovereignty-sensitive pages

## Guardrails & Constraints
- Cultural sensitivity: **high** — do not trivialise or rebrand customary rights
- Never “fix” compliance by moving data offshore for convenience
- HITL required for architecture changes that alter data residency

## References
- fivepanelhat portfolio table
- Portal COMPLIANCE.md (AquaGuard, SoilGuard, Blue-Moon, Sting, Weaver)
- Related skills: `kiwi-edge-architecture`, `service-role-key-protection`, `hub-nextjs-component`
