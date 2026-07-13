---
name: cat-trust-layer
description: Use whenever building, reviewing, or deploying any Coastal Alpine Tech product (Weaver, Blue-Moon-Portal, Sting-Operation-AI, AquaGuard-Portal, SoilGuard-Portal, coastal-alpine-core, Front_Line_Whanau) that will run for, or expose data to, an end user, farmer, or whanau. Enforces the five-layer trust stack (sovereign foundation, data sovereignty and consent, human-in-the-loop oversight, transparency and accountability, community trust) that turns New Zealand's low AI-trust environment into an adoption advantage rather than a barrier. Trigger phrases include trust layer, data transparency, actuator safety, consent card, trust hub, data card, AI trust.
metadata:
  version: "1.0.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-07-13"
  type: guardrail
  requires_hitl: true
  cultural_sensitivity: high
  related_standards: Gold Platinum Diamond Te-Mana-Raraunga release-preflight
---

# CAT Trust Layer

Cross-portfolio governance skill that operationalises the trust stack Coastal Alpine Tech is built on: sovereign local infrastructure at the foundation, data sovereignty and human oversight as the operating layers, transparency and accountability as the proof, and community trust as the outcome. Built in direct response to NZ's 2026 AI-trust data — most Kiwis have used AI but remain cautious, 62% will walk from an organisation over misuse concerns, and Kiwis trust small local businesses to use AI responsibly far more than multinationals. That last point is the whole thesis: this skill exists to make the trust advantage real and auditable, not a slogan.

## Overview

Every CAT product sits on the same five layers. This skill enforces them as guardrails Aether checks and applies during real work, not as a values statement that lives only in a pitch deck.

1. **Sovereign offline-native foundation** — local inference, no cloud round-trip by default.
2. **Data sovereignty & consent** — Te Mana Raraunga aligned controls, visible to the end user.
3. **Human-in-the-loop oversight** — no physical action without human confirmation.
4. **Transparency & accountability** — public, plain-language trust artefacts.
5. **Community trust** — the outcome; earned through the four layers above, never bought with marketing spend.

## When to Use

- Any product or repo (Weaver, Blue-Moon-Portal, Sting-Operation-AI, AquaGuard-Portal, SoilGuard-Portal, coastal-alpine-core, Front_Line_Whanau) approaching pilot or public-facing deployment.
- Any code path that drives a physical actuator (laser targeting, fertigation lockouts, dosing, or similar).
- Any code path where sensor, usage, or personal data leaves a local device or local network.
- Before publishing any public trust-hub page, data card, pitch deck, or LOI/pilot conversation that makes a claim about how the AI behaves.
- Before committing, tagging, or releasing any work that claims compliance with this skill.

## Instructions

1. Identify whether the current task touches (a) actuator control, (b) data collection or transmission, or (c) a public-facing claim about AI behaviour. If any apply, do not mark the task complete until the relevant guardrail below is satisfied.
2. **Actuator control**: confirm a human-confirmation gate sits in the execution path before any physical action fires. This must be enforced in code, not left as a documented convention. There is no config flag that disables it in production.
3. **Data flows**: confirm a `TRUST.md` (or in-product equivalent, e.g. an on-device data card) exists at the repo root, covering what is collected, where it is stored (local by default, any exception explicitly logged and consented to), who can access it, and a working deletion path. Create it as part of the task if missing.
4. **Public claims**: cross-check every claim of "sovereign," "human-reviewed," "offline," or "private" against an implemented, testable guardrail. Do not let marketing language get ahead of what the code actually does.
5. **Before any pilot, LOI, or paid deployment**: confirm the relevant product has a shareable trust-hub page in plain language — what it does, what it doesn't do, how data is handled, and how to reach a human.
6. Log every guardrail check performed in the task summary, in the same style as the `release-preflight` incident log — this skill is the human-facing counterpart to that system, not a duplicate of it.

## Guardrails & Constraints

- No actuator (laser, fertigation valve, or other physical control) fires without an explicit human-confirmation step in the execution path. Non-negotiable, no environment-based override in production.
- No sensor or usage data leaves the local device or local network without informed, revocable consent that is logged and reversible.
- Every product ships a data-transparency artefact before any external pilot — no exceptions for "just a demo."
- No public claim of sovereignty, human review, or offline operation without a corresponding guardrail that is actually implemented and testable by an outside reviewer.
- Any change to a guardrail defined in this skill requires a semver bump, a `references/CHANGELOG.md` entry, and explicit HITL approval, per `aether-skills-ci` convention.
- The Cultural Safety & Sovereignty Overlay in `cat-architectural-standards` applies in full: Te Mana Raraunga governs all data design; Front_Line_Whanau content additionally requires explicit consent and controls for any health-adjacent data, with no PHI handled without them.

## Integration with Other Skills

- Load `aether-core` first for HITL and orchestration rules.
- Load `cat-architectural-standards` alongside this skill to classify the work (Gold / Platinum / Diamond) — trust-layer guardrails apply across all three tiers, they are not tier-specific.
- Load `aether-git-workflow` before committing any change to a guardrail or actuator-control code path.
- Treat `release-preflight` (Aether v0.6.2) as the enforcement mechanism for the human-in-the-loop layer — real incidents get encoded there as preflight checks, this skill defines what must be checked and why.

## Anti-Patterns to Avoid

- Treating this as a marketing checklist rather than enforced code paths.
- Publishing a trust-hub page describing guardrails that are not actually implemented yet.
- Adding a "testing mode" flag that disables human-confirmation in a production build — isolate test environments physically or logically instead.
- Treating community trust as something to buy with ad spend rather than earn through the four layers beneath it.

## Progressive Disclosure

- This `SKILL.md` holds the decision protocol and core guardrails.
- Product-specific templates (`data-card-template.md`, `trust-hub-template.md`) in `assets/` — fill these in per-product.
- Version history lives in `references/CHANGELOG.md`.
