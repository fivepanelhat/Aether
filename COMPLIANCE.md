# COMPLIANCE.md

**Coastal Alpine Tech Limited** | **Product:** Aether
Last updated: 22 July 2026

## Privacy / Security / Governance (fleet mandatory)

**Last reviewed (fleet block):** 22 July 2026

| Pillar | Standard |
| --- | --- |
| **No data sales** | **Personal and customer operational data is not sold to third parties** for ads, data brokerage, or unrelated monetisation. |
| **Privacy** | Designed to operate in accordance with the **New Zealand Privacy Act 2020** (IPPs; IPP 3A awareness). Local-first default; purpose-limited collection; third-party processing only when opt-in and disclosed. |
| **Te Mana Raraunga** | Designed to operate **in accordance with Te Mana Raraunga** Māori data sovereignty principles where Māori / community data interests apply. |
| **NZ AI safety** | Aligned with NZ AI safety / responsible AI posture: human oversight for high-stakes use, transparency of AI processing, Algorithm Charter spirit, no silent training on private customer content without consent. |
| **Security** | No silent exfil; owner-controlled credentials; least privilege; SecOps / red-team cadence where CI is present. |
| **Governance** | HITL for high-stakes; agents draft only; humans sign / send / pay. |
| **Assurance path** | **SOC 2** Type I/II and **ISO/IEC 42001** treated as multi-tenant SaaS **alignment targets**, not claimed certifications unless a formal report is published. |
| **Regions** | Australia, Asia-Pacific, and European frameworks mapped in [`COMPLIANCE_REGIONS.md`](./COMPLIANCE_REGIONS.md) under a **NZ AI safety-first** baseline. |

> This document is **alignment evidence**, not a compliance certificate, audit report, or legal advice.


## Regulatory Mapping

### New Zealand
- Privacy Act 2020 + **IPP 3A** (Privacy Amendment Act 2025) - effective **1 May 2026**  
  Notification required when personal information is collected indirectly.
- Biometric Processing Privacy Code 2025  
  New biometric processing: 3 November 2025  
  Existing biometric processing: 3 August 2026
- Health Information Privacy Code (applies where health / wellbeing data is processed)
- Te Mana Raraunga principles - primary data sovereignty framework

### European Union
- **EU AI Act** - Annex III high-risk obligations enforceable **2 August 2026**
- Relevant high-risk categories:
  - Health decision support
  - Biometrics (remote identification, categorisation, emotion recognition)
  - Critical infrastructure / essential services
- Required: risk management, data governance, technical documentation, human oversight, logging, transparency, post-market monitoring

### International Standards
- **ISO/IEC 42001** - AI Management System (AIMS)  
  Covers AI policy, risk assessment, data governance, human oversight, monitoring, continual improvement
- **SOC 2** - Security, Availability, Confidentiality, Processing Integrity, Privacy  
  Priority for multi-tenant / customer-facing components

### Core Technical Controls (Mandatory)
- Local-first / offline-native processing by default
- Owner-controlled encryption keys
- No silent data exfiltration
- Explicit Human-in-the-Loop (HITL) gates for high-impact and culturally sensitive decisions
- Data residency under New Zealand control

### Scope Notes
- Current systems prioritise offline-native operation and data minimisation.
- Any future multi-tenant or customer-facing features will be assessed against SOC 2 and EU AI Act high-risk requirements before release.

### Limitations
- Not legal advice; not a certification claim.
- Confirm statute application with NZ counsel before commercial shipping claims.
- Agents inform / draft / prepare only; humans advise / sign / file / send / pay.

---

## Product-specific mapping

**Sovereign Agentic Development System**  
Aligned with Te Tiriti o Waitangi and Te Mana Raraunga

---

## Purpose

This document outlines Aether's commitments to data sovereignty, cultural safety, human oversight, security, and responsible development practices. It serves as a reference for developers, reviewers, and partners.

Aether is designed to support high-stakes, community-focused digital platforms - particularly those serving whānau in Aotearoa New Zealand. As such, compliance is not an afterthought but a core design constraint.

---

## 1. Te Mana Raraunga & Māori Data Sovereignty

Aether is built with explicit respect for **Te Mana Raraunga** principles:

- **Rangatiratanga**: Māori retain authority over their data and digital presence.
- **Kaitiakitanga**: Aether supports responsible guardianship of data and knowledge.
- **Whakapapa**: Data and decisions should be understood in relational and historical context.
- **Manaakitanga**: Care and respect for people and communities is prioritised.
- **Kotahitanga**: Work should ultimately serve collective benefit.

**Implementation**:
- Strong preference for local/self-hosted operation.
- Data minimisation by default.
- Clear pathways for cultural review of skills, agents, and outputs that touch Māori data or knowledge.
- No assumption that data can be freely used or moved without explicit consideration of sovereignty.

---

## 2. Human-in-the-Loop (HITL)

Aether operates under a **strong HITL model**:

- The system proposes, plans, and prepares work.
- Humans retain final authority over high-impact actions (code changes, Git operations, sensitive content, cultural decisions).
- Skills and agents can flag when human review is required (`requires_hitl` metadata).
- Cultural sensitivity level (`cultural_sensitivity`) is declared per skill to guide review processes.

Aether is designed to **augment**, not replace, human judgment - especially on matters involving whānau, culture, health-adjacent information, or data sovereignty.

---

## 3. Data Privacy & Sovereignty

- Aether is designed to run **locally or in sovereign environments** wherever possible.
- Skills and tools should minimise data exfiltration.
- Memory systems should support tagging of culturally sensitive or restricted information.
- When working with external services (e.g. LLMs, search), data handling must be transparent and minimised.

---

## 4. Security Practices

Aether follows security-conscious development:

- Input validation and sanitisation on tool and skill inputs.
- Avoidance of hardcoded secrets or credentials.
- Clear separation between development, staging, and production environments.
- Regular review of tools that interact with filesystems, networks, or external APIs.

---

## 5. Cultural Safety

- Skills that may affect Māori or Pacific communities should declare `cultural_sensitivity: medium` or `high`.
- The orchestrator and skills should support inclusive language and avoid assumptions about family structures, cultural practices, or identity.
- When relevant, skills should recommend cultural review before implementation.

---

## 6. Responsible Skill & Agent Development

When creating or modifying skills and agents:

- Skills should be versioned and reviewable.
- Overly broad or high-risk automation should require explicit human approval.
- Skills that interact with sensitive domains (funding, health navigation, cultural knowledge) must include appropriate disclaimers and review pathways.
- Self-improvement features (automatic skill creation) must include guardrails, especially for culturally sensitive areas.

---

## 7. Transparency & Auditability

- Plans, tool calls, and changes should be logged where feasible.
- Memory entries and skill usage should be reviewable.
- Major architectural or skill changes should be documented.

---

## 8. Limitations

Aether is **not**:

- A replacement for professional legal, cultural, or clinical advice.
- A fully autonomous system for high-stakes decisions.
- A finished product - it is under active development.

Users and operators remain responsible for reviewing outputs, especially when they may affect whānau, funding, health navigation, or cultural matters.

---

## Ongoing Commitments

- This document will evolve as Aether develops.
- Feedback from cultural advisors, security reviewers, and community stakeholders is welcomed.
- Aether's design prioritises **sovereignty, care, and accountability** over raw capability or speed.

---

**Maintained as part of the Aether project.**

### Data sales

**We do not sell personal or customer operational data to third parties.**
