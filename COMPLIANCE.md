# Aether Compliance Framework

**Sovereign Agentic Development System**  
Aligned with Te Tiriti o Waitangi and Te Mana Raraunga

---

## Purpose

This document outlines Aether’s commitments to data sovereignty, cultural safety, human oversight, security, and responsible development practices. It serves as a reference for developers, reviewers, and partners.

Aether is designed to support high-stakes, community-focused digital platforms — particularly those serving whānau in Aotearoa New Zealand. As such, compliance is not an afterthought but a core design constraint.

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

Aether is designed to **augment**, not replace, human judgment — especially on matters involving whānau, culture, health-adjacent information, or data sovereignty.

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
- A finished product — it is under active development.

Users and operators remain responsible for reviewing outputs, especially when they may affect whānau, funding, health navigation, or cultural matters.

---

## Ongoing Commitments

- This document will evolve as Aether develops.
- Feedback from cultural advisors, security reviewers, and community stakeholders is welcomed.
- Aether’s design prioritises **sovereignty, care, and accountability** over raw capability or speed.

---

**Maintained as part of the Aether project.**
