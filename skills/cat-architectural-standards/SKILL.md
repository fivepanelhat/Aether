---
name: cat-architectural-standards
version: "1.0.0"
type: decision
requires_hitl: true
description: Use when planning, classifying, reviewing, or executing any work for Coastal Alpine Tech, Aether, the Whānau Preterm Support Hub, Mana Kai, or related projects. Enforces the Gold / Platinum / Diamond maturity model. Choose the correct execution mode, apply HITL gates, and keep all work aligned with sovereign AI, Te Mana Raraunga, and data flywheel principles. Trigger phrases include Gold Standard, Platinum Standard, Diamond Standard, architectural standards, maturity tier, execution mode, Platinum Edge.
status: active
owner: Coastal Alpine Tech
last_updated: "2026-07-11"
---

# CAT Architectural Standards

Top-level decision and governance skill for Coastal Alpine Tech. Operationalises the three hierarchical standards that define how all work is planned, executed, and evaluated.

## Versioning

- Current version is declared in frontmatter `version` (semver).
- On any material change to definitions, decision protocol, HITL gates, or hardware targets, increment the version and update `last_updated`.
- Maintain a short changelog in `references/CHANGELOG.md`.
- Skills that implement the three tool signatures (`gold_standard_execution`, `platinum_recursive_optimization`, `diamond_infrastructure_deploy`) must declare compatibility with a minimum version of this skill.

## The Three Standards

### 1. GOLD STANDARD — Workflow-Native Design
- **Nature**: Process-first, deterministic, linear.
- **Purpose**: Ensure the platform is a direct digital reflection of the real-world industry or community workflow (unbroken data chain, lifecycle-driven modularity).
- **State Machine**: Strictly linear with hard gates (Discovery → Design → Development → Testing → Deployment). Cannot proceed to Phase N+1 without validation of Phase N.
- **When to use**: Feature work, resource content, Hub pages, basic integrations, any work that must mirror a clear real-world process.
- **Agent Skill Trigger**: `gold_standard_execution(current_phase, payload)`

### 2. DIAMOND STANDARD — Enterprise-Grade Foundation
- **Nature**: Production-ready technical blueprint ("Tier 1 in a Box").
- **Purpose**: Guarantee scalability, security, observability, zero-downtime operations, and compliance readiness from day one.
- **Core Elements**: Modern stack (Next.js / TypeScript / Python / Postgres / Redis), IaC (Terraform), containerisation + orchestration (Docker + Kubernetes / EKS Hybrid Nodes), Blue-Green deployments, multi-layered security (VPC, WAF, KMS, JWT, encryption at rest), Sui Web3 trust layer for high-value actions.
- **When to use**: Infrastructure, CI/CD, security hardening, observability, hybrid edge setup, anything that must be enterprise-grade and production-ready.
- **Agent Skill Trigger**: `diamond_infrastructure_deploy(manifest, hardware_target, security_protocol)`

### 3. PLATINUM STANDARD — Intelligent Self-Improving System
- **Nature**: Synthesis of Gold + Diamond elevated by a strategic AI Engine and data flywheel.
- **Purpose**: Turn the platform into a system that gets smarter with every use, creating a durable competitive moat through continuous local learning.
- **Core Elements**: Centralised (or hybrid-edge) AI Engine (Aether agents), strategic data capture across the full workflow, continuous improvement loop (capture → curate → LoRA/PEFT → evaluate → hot-swap), predictive value creation, local fine-tuning on DGX Spark / high-memory edge nodes.
- **When to use**: Agent design, RAG / memory systems, data flywheel implementation, local model fine-tuning, anything that improves the intelligence of the system over time.
- **Agent Skill Trigger**: `platinum_recursive_optimization(objective, seed_vectors, max_iterations)`

**Platinum Edge Extension** (current evolution of Platinum): Hybrid Cloud-Edge architecture using Raspberry Pi 5 16GB + Hailo-10H (field/sensor layer) and NVIDIA DGX Spark GB10 (128GB UMA intelligence hub), orchestrated via EKS Hybrid Nodes, with local data flywheel and NeMo-style PEFT.

## Decision Protocol

When a new task or goal is received:

1. Classify the work into one primary standard (Gold / Platinum / Diamond). Many tasks will touch more than one — declare the primary and secondary.
2. State the classification clearly before proceeding.
3. Apply the corresponding execution rules:
   - Gold → Use linear phase gates and workflow mapping.
   - Diamond → Enforce security, observability, IaC, and production readiness.
   - Platinum → Design for learning loops, data capture, and continuous improvement.
4. Apply mandatory HITL gates (see below).
5. Reference this skill in any Architecture Decision Record or major plan.

## HITL Gates (Non-Negotiable)

- Any change that alters the classification of a major system or introduces a new standard → HITL required.
- Any work involving health content, cultural content, Te Mana Raraunga claims, or funding pathways → HITL + cultural review readiness.
- Any infrastructure or Diamond-level change that affects production, security posture, or data sovereignty → HITL.
- Any Platinum flywheel or local fine-tuning work that will touch real farm or whānau data → HITL.
- Before committing, tagging, or releasing any work that claims Gold / Platinum / Diamond compliance.

## Cultural Safety & Sovereignty Overlay (Applies to All Tiers)

Every standard inherits these constraints:

- Te Tiriti o Waitangi principles (rangatiratanga, kaitiakitanga, manaakitanga, etc.) are architectural requirements, not optional features.
- Te Mana Raraunga principles must be respected in data design, storage, and agent behaviour.
- No PHI or sensitive health data without explicit consent and proper controls.
- All public-facing content must carry appropriate medical / funding disclaimers.
- Accessibility (WCAG 2.2 AA) and low-bandwidth considerations are Diamond-level requirements that also apply to Gold and Platinum work.

## Practical Usage Patterns

**When planning a new feature or page**  
Start with Gold (map the real workflow) → ensure Diamond foundation is ready → design Platinum learning hooks if relevant.

**When reviewing existing work**  
Ask: Is this Gold-aligned (workflow)? Is the foundation Diamond-grade? Does it contribute to or block the Platinum flywheel?

**When choosing hardware or infrastructure**  
- Field sensors & actuators → Raspberry Pi 5 16GB + Hailo (supports Gold data capture).  
- Intelligence hub / local fine-tuning → DGX Spark trajectory (enables full Platinum).  
- Control plane → AWS EKS Hybrid Nodes (Diamond).

**When writing Architecture Decision Records**  
Explicitly declare which standard(s) the decision advances or protects.

## Integration with Other Skills

- Use `git-workflow` for any Diamond-level release or infrastructure changes.
- Use `hub-nextjs-component` for Hub-specific Gold work on UI components and accessibility.
- Use `skill-creator` when creating or refining skills that implement parts of these standards.
- Use `release-preflight` and `release-engineering` for Gold/Diamond-aligned release gates.
- Future skills that implement the three tool signatures (`gold_standard_execution`, `platinum_recursive_optimization`, `diamond_infrastructure_deploy`) must declare compliance with this skill (minimum version stated in their metadata).

## Anti-Patterns to Avoid

- Treating Platinum as "just add more AI" without the Gold workflow foundation and Diamond reliability.
- Claiming Diamond status without proper security, observability, and IaC.
- Building pure Gold linear systems that cannot later feed a Platinum flywheel.
- Ignoring cultural sovereignty constraints when applying any of the three standards.
- Skipping the classification step and jumping straight into code.

## Progressive Disclosure

- This SKILL.md contains the decision protocol and core definitions.
- Detailed reference materials live in `references/` (including Skills-to-Tiers Mapping and CHANGELOG).
- Load references only when deep technical or historical detail is required.

## Related References

- `references/Skills_to_Tiers_Mapping.md` — full mapping of Aether skills to Gold / Platinum / Diamond.
- `references/CHANGELOG.md` — version history for this skill.