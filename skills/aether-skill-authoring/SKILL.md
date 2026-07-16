---
name: aether-skill-authoring
description: Use when creating, updating, or refining new agent skills for Aether or the Whānau Preterm Support Hub. Provides Hub-specific guidance on skill structure, frontmatter, progressive disclosure, HITL integration, cultural safety considerations, and production-quality authoring practices. Load this skill before authoring any new skill.

metadata:
  version: "1.0.0"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-07-16"
---

# Aether Skill Authoring

This skill adapts and extends general skill creation best practices for the specific needs of Aether and the Whānau Preterm Support Hub NZ. It ensures every new skill is production-ready, maintainable, culturally safe where relevant, and optimised for reducing context switching.

## When to Create a New Skill

Create a new skill when you identify:
- Repeated patterns or procedures that are currently re-explained in every conversation.
- Project-specific workflows (Hub component patterns, agent scaffolding, GitHub processes, whānau resource generation).
- Domain expertise that needs to be consistently applied (accessibility standards, Te Tiriti alignment checks, medical disclaimer handling).
- Complex multi-step processes that benefit from structured guidance and templates.

**Do not** create skills for general knowledge the model already possesses well.

## Skill Structure (Standard for Aether)

Every skill must follow this layout:

```
skill-name/
├── SKILL.md              # Required
├── scripts/              # Optional but recommended for deterministic actions
├── references/           # Optional for longer documentation
└── assets/               # Optional for templates and reusable files
```

## Frontmatter Requirements

The `description` field is critical — it is the only content shown before the skill is loaded.

Requirements:
- Write as a plain YAML scalar (no quotes, no colon-space `:` , no angle brackets).
- Clearly state both **what** the skill does and **when** it should be used.
- Include trigger phrases the user is likely to say.
- Keep under 1,024 characters.

Example structure:
```yaml
---
name: example-skill-name
description: Use when the user wants to [specific action]. Handles [key capabilities]. Always [important constraint or HITL rule].
---
```

## Body Writing Guidelines

- Write in clear **imperative** form ("Plan the work...", "Present the diff for approval...").
- Be concise — every paragraph must justify its token cost.
- Focus only on what the model does **not** already know or what needs to be applied consistently for this project.
- Include the mandatory HITL gates relevant to the skill's domain.
- Reference `aether-core` principles (especially cultural safety, accessibility, and disclaimers for health-related content).
- For skills that touch whānau-facing content, explicitly require appropriate disclaimers and cultural review readiness.

## Progressive Disclosure Strategy

Design every skill with three levels in mind:
1. **Metadata** (name + description) — ~100 tokens, always visible.
2. **SKILL.md body** — Load only when relevant; target under 5,000 tokens.
3. **references/** and **assets/** — Load on demand for deeper detail or templates.

If the body approaches 500 lines, move detailed content into `references/` files.

## HITL Integration

Every skill that can affect production code, health information, cultural content, or GitHub state **must** include explicit approval gates. Reference the protocols in `aether-core` and `aether-git-workflow`.

## Cultural Safety & Hub Alignment

When authoring skills that may generate or influence content for whānau:
- Embed requirements for Te Tiriti-aligned reasoning (rangatiratanga, kaitiakitanga, manaakitanga).
- Require clear disclaimers on any health, funding, or support pathway information.
- Design for accessibility (WCAG 2.2 AA) and low-bandwidth scenarios from the start.
- Make it easy for future cultural reviewers to understand and extend the skill.

## Authoring Process (Recommended)

1. Identify the repeated pain or high-leverage pattern.
2. Clarify concrete trigger phrases and example tasks.
3. Decide on required resources (scripts, references, assets).
4. Initialise the skill using the standard init script.
5. Write a strong frontmatter description first.
6. Draft the body focused on non-obvious, project-specific guidance.
7. Add templates or checklists in `references/` or `assets/`.
8. Validate the skill structure.
9. Test the skill on a real task and iterate based on gaps.

## Anti-Patterns to Avoid

- Duplicating general model knowledge.
- Putting trigger information in the body instead of the description.
- Creating overly long SKILL.md files without using references.
- Nesting references.
- Creating skills without clear HITL gates when they affect production or sensitive content.
- Naming skills inconsistently or using names that do not match the directory.
