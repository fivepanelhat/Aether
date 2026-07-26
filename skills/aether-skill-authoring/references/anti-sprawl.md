# Aether Skill Anti-Sprawl Policy

**Status:** Active guidance  
**Applies to:** All skill creation, update, composition, and retirement decisions in Aether / Coastal Alpine Tech  
**Related skills:** `aether-skill-authoring`, `aether-trajectory-capture`, `aether-skill-composition`

---

## Purpose

Prevent uncontrolled proliferation of redundant, low-quality, or unowned skills (skill sprawl).  
A lean, high-signal skill library is a prerequisite for progressive disclosure, ordered shortlists, and reliable trajectory capture.

Sprawl is the failure mode that occurs when creation is easy and curation is weak.

---

## Standing Rules

1. **Update existing > create new**  
   Prefer improving or extending an existing skill over adding a near-duplicate.

2. **Demand management first**  
   Before creating any skill, check whether an existing skill (or short composition of existing skills) already covers the need adequately.

3. **Fewer is better**  
   A smaller set of precise, well-described skills outperforms a large, poorly differentiated library.

4. **Ownership is required**  
   Every skill must have a clear owner (person or role) recorded in metadata.

5. **Lifecycle is explicit**  
   Skills have a status: `active` | `experimental` | `deprecated`.  
   Deprecated skills remain readable for history but should not be selected by default.

6. **HITL on consequential creation**  
   New skills that touch production code, health information, cultural content, funding, sovereignty, or Git state require explicit human approval before landing.

---

## Pre-Creation Checklist

Use before any new skill is proposed or written:

- [ ] Is there already a skill that covers this need (even partially)?
- [ ] Can an existing skill be updated or generalised instead?
- [ ] Is the need recurring and non-trivial (not a one-off)?
- [ ] Is the proposed skill’s description precise enough for reliable Tier-1 triggering?
- [ ] Does the skill introduce clear HITL gates where required?
- [ ] Who owns this skill after it is created?
- [ ] What is the retirement or review condition?

If the first two answers are “yes, an existing skill can cover this”, stop and update instead.

---

## Composition Discipline

When using `aether-skill-composition`:

- Target 2–5 skills in a shortlist.
- Prefer skills that already encode the necessary safety / cultural / sovereignty constraints.
- Prefer `status: active` skills; exclude `deprecated` skills from default shortlists.
- Avoid proposing near-duplicates in the same shortlist.
- Record the final shortlist (including user edits) so trajectory capture can learn from good compositions.

---

## Trajectory Capture Discipline

When using `aether-trajectory-capture`:

- Strongly prefer proposing an **update** to an existing skill over a brand-new skill.
- Apply the pre-creation checklist before any new skill is written.
- Always require HITL approval before writing.

---

## Lifecycle & Retirement

- Skills should be reviewed periodically (especially experimental ones).
- When a skill is superseded or no longer useful, mark it `deprecated` rather than deleting it immediately.
- Deprecated skills should not appear in default shortlists.
- Ownership includes responsibility for eventual retirement or hand-over.

---

## Anti-Patterns (Do Not)

- Creating a new skill because it is easier than reading existing ones.
- Allowing multiple near-identical skills to coexist without merge or deprecation.
- Leaving skills without an owner.
- Letting experimental skills become permanent by default.
- Loading or proposing the entire skill library for a single task.
- Treating skill creation as cost-free.

---

## Success Signal

The skill library grows slowly, stays high-signal, and most new capability arrives as updates to existing skills rather than net-new entries.
