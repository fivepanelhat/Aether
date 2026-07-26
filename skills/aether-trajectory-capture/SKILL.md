---
name: aether-trajectory-capture
description: Use when a multi-step agent run has succeeded and the workflow should be turned into a reusable skill, or when the user asks to capture, save, or extract a skill from a successful trajectory. Handles trajectory packaging, novelty checks, draft skill generation, and mandatory HITL approval before any skill is written. Prefer updating an existing skill over creating a new one.
metadata:
  version: "0.1.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-07-26"
  related_skills:
    - aether-skill-authoring
    - aether-core
    - aether-hitl-protocol
---

# Aether Trajectory Capture (v0.1.0)

Turn successful agent trajectories into permanent, high-quality skills.

This skill implements the learning flywheel: every verified success can raise the capability of the entire system. It is deliberately conservative — no skill is written without explicit human approval.

## Core Principle

A successful trajectory is the highest-quality source material a skill can have.  
Capture it, refine it under HITL, version it, and make it reusable.

## When to Use

Trigger this skill when:

- A multi-step task has reached a clear successful outcome (user confirmed or objective criteria met).
- The user explicitly asks to “capture this”, “save this workflow”, “turn this into a skill”, or similar.
- The trajectory involved non-trivial reasoning, tool use, or judgment calls that are likely to recur.
- An existing high-value domain run (grants, security, Hub processes, edge architecture, etc.) completed successfully.

Do **not** trigger for trivial single-step answers or failed runs.

## Preferred Mode: Semi-Automatic Offer

After a successful multi-step run, the orchestrator should offer:

> “Successful multi-step trajectory detected. Capture as skill?  
> [Yes – new skill] / [Update existing skill] / [No]”

Only proceed on explicit user choice.

## Process

### 1. Package the Trajectory

Create a compact structured package:

```yaml
trajectory:
  id: traj-YYYYMMDD-HHMMSS-<short-hash>
  task_summary: "one-sentence description of the goal"
  success_criteria: "how success was judged"
  steps:
    - step: 1
      thought: "key reasoning"
      action: "tool call or decision"
      observation: "result"
      key_decision: "why this path was chosen"
  final_outcome: "what was delivered"
  failure_modes_avoided: []
  tools_used: []
  skills_already_loaded: []
  human_feedback: "any explicit quality comments from the user"
```

Keep the package tight. Prefer structured data over long free-text transcripts.

### 2. Novelty & Overlap Check

Before drafting a skill:

- Search existing skills for substantial overlap.
- Prefer **updating an existing skill** over creating a new one.
- Only propose a brand-new skill when the trajectory introduces genuinely new procedural knowledge.

### 3. Draft the Skill

Using the trajectory package and the rules in `aether-skill-authoring`:

- Write a precise Tier-1 description (the only signal the agent will see initially).
- Produce a clean, imperative body that captures the reusable procedure, decision points, and HITL gates.
- Move bulk detail into `references/` if needed.
- Record the source trajectory ID in the skill’s CHANGELOG.

### 4. Mandatory HITL Gate

Present to the user **before any file is written**:

- Proposed skill name + description
- Full draft body (or clear diff if updating an existing skill)
- Overlap analysis (“new skill” vs “update to X”)
- Any cultural, health, sovereignty, or high-stakes considerations
- Explicit request for approval

**No skill is committed without clear user approval.**

### 5. Finalise & Store

On approval:

1. Write or update the skill under `skills/` following `aether-skill-authoring` structure and validation rules.
2. Update the skill’s `CHANGELOG.md` with a reference to the source trajectory ID.
3. Optionally store the raw trajectory package under `references/trajectories/` (or equivalent) for audit and future analysis.
4. Confirm to the user what was created or updated.

## Quality Gates (Prevent Sprawl)

A trajectory may only become a skill if it passes:

| Gate | Requirement |
|------|-------------|
| Novelty | Does not substantially duplicate an existing skill |
| Generality | Procedure is useful beyond this single instance |
| Description precision | Description alone is sufficient for reliable Tier-1 triggering |
| Safety | All high-stakes actions have explicit HITL gates |
| Size | Body respects progressive-disclosure limits |
| Attribution | Source trajectory ID is recorded |

Fail any gate → recommend an update to an existing skill or discard.

## Relationship to Other Skills

- **aether-skill-authoring** remains the single source of truth for how skills are structured, validated, and written.
- This skill is responsible only for *extracting and proposing* from real trajectories.
- All final writing and validation must obey `aether-skill-authoring`.
- High-stakes domains still require the normal HITL and cultural safety rules from `aether-core` and `aether-hitl-protocol`.

## Anti-Patterns

- Capturing failed or low-quality runs.
- Creating a new skill when a small update to an existing one would suffice.
- Writing a skill without showing the draft to the user.
- Storing long raw transcripts instead of compact structured packages.
- Skipping the novelty / overlap check.
- Treating trajectory capture as fully automatic with no human gate.

## Success Metric

The skill library grows with high-quality, battle-tested procedures while remaining lean and precisely triggered.
