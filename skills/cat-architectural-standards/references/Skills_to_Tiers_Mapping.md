# Skills-to-Tiers Mapping
**Skill:** cat-architectural-standards  
**Version:** 1.0.0  
**Date:** 11 July 2026  
**Purpose:** Map every current and emerging Aether skill to the Gold / Platinum / Diamond architectural standards so that work is correctly classified, gaps are visible, and the maturity model becomes operational.

---

## How to Read This Document

| Tier | Primary Role | Typical Work |
|------|--------------|--------------|
| **GOLD** | Workflow-Native Design | Process mapping, feature development, content, linear delivery, real-world lifecycle alignment |
| **DIAMOND** | Enterprise-Grade Foundation | Security, CI/CD, infrastructure, observability, production readiness, compliance |
| **PLATINUM** | Intelligent Self-Improving System | Agent design, data flywheels, local learning, RAG/memory, recursive optimisation |

Many skills serve more than one tier. Primary and secondary classifications are shown.

---

## Current Skills Inventory & Mapping

### Core Orchestration Layer

| Skill | Primary Tier | Secondary | Notes / Role |
|-------|--------------|-----------|--------------|
| `aether-core` | **Platinum** | Gold, Diamond | Top-level orchestrator. Enforces HITL, cultural safety, and coordinates all other skills. The living embodiment of the Platinum AI Engine. |
| `cat-architectural-standards` (new) | **All three** | — | Meta-skill. Classifies work into Gold / Platinum / Diamond and enforces the maturity model. Must be loaded for any significant planning or architectural decision. |
| `aether-skill-authoring` | Diamond + Platinum | Gold | Ensures new skills are production-grade (Diamond) and can contribute to learning/improvement (Platinum). |

### Delivery & Governance (Strong Diamond)

| Skill | Primary Tier | Secondary | Notes / Role |
|-------|--------------|-----------|--------------|
| `aether-git-workflow` | **Diamond** | Gold | Safe Git/GitHub operations, conventional commits, PR process, release safety. Core Diamond practice. |
| `release-preflight` (emerging) | **Diamond** | — | 7-point validation (visibility, sensitive files, tag collision, monotonic versioning, tests, clean tree). Hard Diamond gate. |
| `keyword-consistency` (emerging) | Diamond | Gold | Enforces consistent naming (hardware standards, terminology) across repos — supports both clean Diamond foundations and Gold clarity. |

### Product & Platform (Gold + Platinum)

| Skill | Primary Tier | Secondary | Notes / Role |
|-------|--------------|-----------|--------------|
| `aether-whanau-hub-architecture` | **Gold** | Platinum, Diamond | Deep knowledge of Hub architecture, agent fleet, cultural safety, Te Tiriti alignment, Supabase/RLS, RAG. Primary Gold workflow mapping for the Hub; also feeds Platinum agents and requires Diamond security. |
| `hub-nextjs-component` | **Gold** | Diamond | Production-ready Next.js / shadcn / accessibility components for Hub UI. Strong Gold (user workflow) + Diamond (accessibility, security, performance). |
| `aether-ui-ux-platform` | Gold | Diamond | UI/UX review frameworks, visual standards, accessibility auditing. Supports Gold user experience and Diamond quality. |

### Domain & Vertical Skills

| Skill | Primary Tier | Secondary | Notes / Role |
|-------|--------------|-----------|--------------|
| `nz-sme-ai-agents` | **Gold** | Platinum | Patterns for NZ SME verticals (Construction, Cafes, Retail, Tourism, etc.). Directly supports Gold workflow-native design for multi-vertical expansion. Can feed Platinum agent fleets. |

### Supporting / General Skills (Context)

| Skill / Capability | Primary Tier | Secondary | Notes |
|--------------------|--------------|-----------|-------|
| Document generation (docx, pdf, pptx, xlsx) | Gold | Diamond | Used to produce Gold-aligned deliverables and Diamond-grade documentation. |
| Media processing (ffmpeg) | Gold / Diamond | — | Supports content and operational needs. |
| Memory & personalisation | Platinum | — | Supports continuous improvement and personalisation loops. |

---

## Coverage Analysis

### Strengths (What We Already Have)

- **Platinum orchestration** is mature (`aether-core` + multi-agent fleet design).
- **Gold workflow mapping** for the Hub and multi-vertical thinking is strong.
- **Diamond foundations** (Git safety, release-preflight, CI hardening, accessibility) are in place or rapidly maturing.
- Cultural safety and Te Mana Raraunga are embedded across tiers rather than bolted on.

### Gaps & Opportunities

| Gap | Recommended Action | Priority |
|-----|--------------------|----------|
| Explicit `gold_standard_execution` tool / skill | Create thin orchestrator skill that enforces the 5-phase linear pipeline | High |
| Explicit `platinum_recursive_optimization` skill | Formalise the 5-pillar / data flywheel loop as a callable skill | High |
| Explicit `diamond_infrastructure_deploy` skill | Codify hybrid edge + EKS Hybrid Nodes + security protocol as a skill | Medium-High |
| Full Platinum Edge hardware skill | Skill that knows RPi field layer + DGX Spark intelligence hub + power/cooling/networking constraints | Medium |
| Cultural Guardrails as first-class Platinum component | Integrate NeMo Guardrails-style rules + Te Tiriti Colang policies into Platinum layer | High |
| Observability & SRE skill (Diamond) | Dedicated skill for Prometheus/Grafana, DCGM, logging, alerting standards | Medium |
| Data Flywheel instrumentation skill | Capture → Curate → Fine-tune → Evaluate → Hot-swap as a repeatable process | High |

---

## Recommended Skill Evolution Path (Next 90 Days)

1. **Immediately**  
   - Commit and activate `cat-architectural-standards`  
   - Keep this mapping document living and update it with every new skill

2. **Days 1–30**  
   - Create thin `gold_standard_execution` skill (5-phase gated pipeline)  
   - Strengthen `release-preflight` and `keyword-consistency` as permanent Diamond skills

3. **Days 31–60**  
   - Create `platinum_data_flywheel` (or full recursive optimisation) skill  
   - Begin formalising Platinum Edge hardware constraints as a skill or reference

4. **Days 61–90**  
   - Create `diamond_infrastructure_deploy` skill (hybrid EKS + security protocols)  
   - Embed cultural safety rules more deeply into Platinum agent execution

---

## How Agents Should Use This Mapping

When Aether Summit (or any specialist agent) receives a task:

1. Load `cat-architectural-standards`.
2. Classify the task (primary + secondary tiers).
3. Load the relevant skills from this mapping.
4. Explicitly state the classification and which skills are being applied.
5. Enforce the HITL gates belonging to the highest-risk tier involved.

This turns the Gold / Platinum / Diamond model from documentation into a living operating system.

---

## Living Document Status

This mapping must be updated whenever:
- A new skill is created or significantly revised
- A skill’s primary role shifts
- A major architectural decision changes the balance between tiers

**Owner:** Coastal Alpine Tech  
**Last Updated:** 11 July 2026  
**Next Review:** After first 30 days of the 30-60-90 plan or when a new skill is added.