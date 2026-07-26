---
name: aether-skill-composition
description: Use when a non-trivial task needs an ordered shortlist of skills before execution, or when the user asks which skills to use, how to sequence them, or to plan the skill set for a goal. Produces a small ordered shortlist (typically 2–5 skills) from Tier-1 metadata, respects progressive disclosure, and applies HITL for medium and high-stakes work. Prefer fewer, better-ordered skills over broad loading.
metadata:
  version: "0.1.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-07-27"
  related_skills:
    - aether-skill-authoring
    - aether-trajectory-capture
    - aether-core
    - aether-hitl-protocol
---

# Aether Skill Composition (v0.1.0)

Produce a small, ordered shortlist of skills for the current task.

This skill sits between goal understanding and skill loading. It improves selection quality without defeating progressive disclosure or token efficiency.

## Core Principle

A good shortlist is better than a large library.  
Prefer 2–5 precisely chosen, ordered skills over broad retrieval or loading everything.

## When to Use

Trigger this skill when:

- The task is non-trivial (multi-step, multi-domain, or high-stakes).
- The user asks “which skills should we use?”, “plan the skills”, “what order?”, or similar.
- The orchestrator needs a clear skill plan before heavy execution.
- A previous attempt failed partly because the wrong skills were loaded.

Do **not** trigger for trivial single-skill or purely conversational turns.

## Preferred Behaviour

**Default for medium and high-stakes work**  
Produce the shortlist and present it for confirmation or light editing before full skill bodies are loaded.

**High-confidence + low-stakes**  
May proceed with the shortlist automatically, while still recording it for later trajectory capture.

**User override**  
Always allowed. The user may add, remove, or reorder skills.

## Process

### 1. Restate the Goal

Produce a one-sentence `task_summary` that captures the user’s intent clearly.

### 2. Generate Candidates

Using only Tier-1 metadata (skill name + description):

- Identify skills that directly address the core goal.
- Include supporting, validation, safety, or finalisation skills where needed.
- Consider conversation history and any known successful past trajectories.
- Do **not** load full skill bodies at this stage.

### 3. Produce the Ordered Shortlist

Emit a compact structured shortlist:

```yaml
shortlist:
  task_summary: "one-sentence restatement of the goal"
  skills:
    - name: skill-name
      rank: 1
      reason: "why this skill is needed at this position"
      expected_role: "primary | supporting | validation | finalisation"
    - name: ...
      rank: 2
      ...
  composition_notes: "any sequencing or dependency observations"
  confidence: "high | medium | low"
  fallback: "what to do if the shortlist proves insufficient"
```

**Size rules**
- Target 2–5 skills.
- Hard ceiling approximately 7.
- Prefer fewer skills over more.

**Ordering rules**
- Primary skill(s) first.
- Supporting and validation skills in logical sequence.
- Finalisation / reporting skills last when relevant.
- Respect likely data or control flow (output of one becomes useful input to the next).

### 4. HITL Gate

| Situation | Action |
|-----------|--------|
| High confidence + low stakes | May proceed; still record the shortlist |
| Medium confidence or complex task | Present shortlist and invite confirmation / edits |
| High stakes (health, cultural content, production code, funding, sovereignty, Git state) | Always present shortlist and require explicit approval before loading full skill bodies |

When presenting, show:

- The ordered list with brief reasons
- Confidence level
- Any notable composition notes
- Clear invitation to accept, edit, or reject

### 5. Hand-off

Once the shortlist is accepted (or auto-accepted under low-stakes rules):

- The normal progressive-disclosure mechanism loads full skill bodies only as each skill is actually needed.
- Execution proceeds under the usual HITL rules of the individual skills and `aether-core`.
- After a successful multi-skill run, `aether-trajectory-capture` may later turn the composition + trajectory into an improved skill or an update.

## Quality Rules

- Prefer existing, well-described skills over inventing new ones.
- Avoid proposing near-duplicate skills; choose the more specific or higher-quality one.
- Prefer skills that already encode required HITL, cultural safety, or sovereignty constraints when the task touches those domains.
- Keep the shortlist explanation concise — every token must justify itself.
- Record the final shortlist (including any user edits) in the run context so trajectory capture can learn from good compositions.

## Relationship to Other Skills

```
User task
    ↓
aether-skill-composition     ← this skill (ordered shortlist)
    ↓
Progressive disclosure       ← loads full bodies only when needed
    ↓
Execution + individual skill HITL
    ↓
(Optional) aether-trajectory-capture
```

- `aether-skill-authoring` remains the authority on how skills are structured and validated.
- `aether-trajectory-capture` remains the authority on turning successful runs into skills.
- This skill is responsible only for *selection and ordering* before execution.

## Anti-Patterns

- Loading the entire skill library into context.
- Producing long unordered lists of skills.
- Skipping the shortlist on high-stakes work.
- Treating the shortlist as a rigid program that cannot be overridden by the user.
- Using full skill bodies (Tier 2/3) during shortlist generation.
- Creating new skills on the fly instead of composing existing ones.

## Success Metric

Higher success rate and lower token cost on multi-skill tasks, with shortlists that humans rarely need to heavily edit.
