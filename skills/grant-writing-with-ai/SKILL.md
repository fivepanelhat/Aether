---
name: grant-writing-with-ai
description: Use when discovering, assessing, drafting, or reviewing grant and funding applications with AI assistance under Coastal Alpine Tech standards. Handles fit scoring, evidence mapping, claim-tier discipline, Te Mana Raraunga alignment, and HITL before any submission. Strengthens the existing grants-agent. Trigger phrases include grant writing, funding application, draft proposal, grant reinforcement, TPK application, New to R and D, funding narrative.
metadata:
  version: "0.1.0"
  status: design-target
  owner: Coastal Alpine Tech
  last_updated: "2026-07-28"
  tier: funding
  hitl_level: L2 on any external submission
  cultural_sensitivity: high
---

# Grant Writing with AI

## Purpose

Provide a disciplined, evidence-based process for using AI to support grant and funding applications while protecting authenticity, claim-tier integrity, and cultural safety. This skill strengthens and extends the existing `grants-agent` and `kaitiaki-grant-lifecycle` rather than replacing them.

## When to Use

- Assessing fit of a funding opportunity against CAT capabilities and evidence.
- Drafting or refining narratives, work packages, and budgets.
- Mapping CAT controls to funder language (AI Strategy, TPK priorities, Te Mana Raraunga, etc.).
- Preparing reinforcement links and footnotes.
- Reviewing a draft before human submission.

## Core Discipline

1. **Evidence before eloquence**  
   Every claim must map to a real CAT artefact, control, or measured result. If evidence is only Design-target, the language must say so.

2. **Claim-tier obedience**  
   L1 Designed language only until scorecards and runtime evidence support higher tiers. Never invent success rates, certifications, or customer results.

3. **Funder language → CAT bridge**  
   Use the official instrument as the primary source. Then add a precise CAT bridge sentence that shows how we implement the requirement.

4. **Cultural and partnership integrity**  
   Māori Development Fund and iwi-related pathways require authentic partnership or kaitono structure. No extractive “add Māori later” framing.

5. **HITL before send**  
   AI prepares. Humans review, approve, and submit. No autonomous submission.

## Standard Workflow

1. **Discover & fit-score**  
   Use current FUNDING_TRACKER and opportunity briefs. Score against capability, evidence maturity, and partnership readiness.

2. **Gather evidence**  
   Pull from GRANT-REINFORCEMENT, alignments, scorecards, architecture docs, and pilot plans. Note the claim tier of each piece.

3. **Draft structure**  
   Follow the funder’s template or the standard sections (problem, solution, outcomes, capability, budget, risks, sustainability).

4. **Write with bridges**  
   For every key claim, cite the external instrument and the internal CAT control.

5. **Risk & honesty pass**  
   Explicitly state what is Design-target, what is planned, and what is already running. Remove any over-claim.

6. **HITL review**  
   Founder + relevant specialists (Cultural Advisor for Māori pathways, Finance for budgets) must approve before submission.

7. **Update tracker**  
   Record status, date, and evidence location after submission or decision.

## Key Artefacts to Reference

- `docs/alignments/GRANT-REINFORCEMENT.md` (v0.2.0+)
- `FUNDING_TRACKER.md` and opportunity briefs
- Scorecards and CLAIM-REGISTER
- Te Mana Raraunga and NZ AI safety skills
- Architecture and pilot plans (for evidence of delivery path)

## HITL Requirements

- Any external grant, LOI, or formal proposal requires explicit founder (or delegated) approval.
- Cultural Advisory review is mandatory for TPK Māori Development Fund, Kotahitanga, or iwi-partnered applications.
- Budget and co-funding statements require Finance review.

## Anti-Patterns

- Copy-pasting generic AI grant text without CAT-specific evidence.
- Claiming “full compliance”, “certified”, or “proven ROI” without supporting scorecard tier.
- Treating partnership requirements as optional.
- Submitting without human review.
- Double-counting the same evidence across multiple concurrent applications without coordination.

## Relationship to Existing Skills

- Directly strengthens `grants-agent` and `kaitiaki-grant-lifecycle`.
- Depends on `GRANT-REINFORCEMENT`, funding matrices, and alignment libraries.
- Uses `nz-data-sovereignty-for-developers` and `aether-nz-ai-safety` for sovereignty and safety narratives.

## Success Criteria

A user of this skill should be able to:

1. Produce a fit assessment that honestly reflects current evidence maturity.
2. Draft a narrative that correctly maps funder language to CAT controls.
3. Maintain strict claim-tier discipline throughout the document.
4. Hand a complete draft to a human for final review and submission with clear notes on remaining risks.
5. Update the funding tracker accurately after the interaction.

## Version & Status

- Version: 0.1.0
- Status: Design-target (L1)
- Next: Add concrete proposal section templates and a pre-submission checklist after first full application cycle.
