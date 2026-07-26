---
name: aether-skill-authoring
description: Use when creating, updating, or refining agent skills for Aether, the Whānau Preterm Support Hub, or any Coastal Alpine Tech project. Encodes progressive disclosure, the successful-run-to-skill workflow, recursive improvement loops, HITL gates, cultural safety, and token-efficient authoring. Load this skill before authoring or improving any skill.
metadata:
  version: "1.1.1"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-07-26"
  source_insights: "Greg Isenberg + Ras Mic (Apr 2026); HyperAgent/Howie Liu; IBM Technology – What AI Agent Skills Are and How They Work (2026)"
---

# Aether Skill Authoring (v1.1.1)

This skill turns the highest-leverage patterns from frontier agent practice into a concrete, production-ready process for Aether and CAT.

**Core principle:** Skills are the primary lever. Models are already good. The differentiator is the quality, progressive disclosure, and continuous improvement of the skills you give them.

## 1. Progressive Disclosure (Non-Negotiable)

Design every skill in three layers:

1. **Metadata only** (name + description) — always present in context. Keep the description under ~150–200 tokens. This is the only thing the agent sees until it decides the skill is needed.
2. **SKILL.md body** — loaded only when the agent selects the skill. Target under 4,000–5,000 tokens. Imperative, project-specific, no general knowledge.
3. **references/** and **assets/** — loaded on demand for deep detail, templates, checklists, or examples.

Never put trigger phrases or “when to use” information only in the body. The description must carry the full decision signal.

This pattern saves thousands of tokens per conversation compared with always-on agent.md / CLAUDE.md files.

See also: `references/industry-practices.md` for the three-tier model as explained by IBM Technology and the emerging open standard.

## 2. The Highest-Leverage Authoring Method

Do **not** write skills abstractly from first principles.

### Preferred workflow (Successful Run → Skill)

1. Walk the agent through a real, concrete task step-by-step until you reach a successful outcome.
2. Once the workflow works, instruct the agent:
   > “Write a clean, reusable skill from the exact process we just followed. Capture the decisions, order of operations, HITL gates, and failure modes we encountered.”
3. Review the generated skill, tighten the description, move bulk content into references/ if needed, and validate structure.
4. Test the new skill on a second similar task.

This produces skills grounded in actual successful context rather than theoretical instructions.

## 3. Recursive Improvement Loop

Skills are never finished. Treat them as living playbooks.

When a skill produces a poor or incomplete result:

1. Capture the failure (what went wrong, what the desired outcome was).
2. Feed it back to the agent with the current skill loaded:
   > “This skill produced X. The correct outcome was Y. Update the skill so this class of failure does not recur.”
3. Have the agent propose a precise diff to the SKILL.md (and any references).
4. Approve and apply the update.
5. Re-test.

This turns every failure into permanent institutional knowledge.

## 4. When to Create a New Skill

Create a skill only when you see:

- A repeated multi-step procedure that is currently re-explained.
- Project-specific patterns (Hub UI, agent scaffolding, grants workflow, edge architecture, security hardening).
- Domain constraints that must be applied consistently (Te Tiriti checks, medical disclaimers, accessibility, data sovereignty).
- Complex workflows that benefit from structured guidance + templates.

**Do not** create skills for general knowledge the model already handles well.

## 5. Required Structure

```
skill-name/
├── SKILL.md                 # Required
├── references/              # Optional – long docs, checklists, examples
│   ├── CHANGELOG.md         # Recommended for versioned skills
│   └── industry-practices.md # Optional reference for alignment notes
├── scripts/                 # Optional – deterministic helpers
└── assets/                  # Optional – templates, sample files
```

## 6. Frontmatter Rules (Description Quality is Critical)

- `description` is the single most important field. It is the **only** signal the agent sees at Tier 1.
- Write it as a clear “Use when…” statement that includes both capability and concrete trigger phrases.
- The description must be precise enough that an LLM can reliably decide “this skill applies” from the description alone.
- Keep it a plain YAML scalar (avoid complex quoting).
- Include key constraints (HITL, cultural safety, sovereignty) in the description when they are load-bearing.
- Always include version, status, owner, and last_updated in metadata.

Vague descriptions cause missed or incorrect triggering.

## 7. Body Guidelines

- Write in clear imperative form.
- Every paragraph must justify its token cost.
- Focus exclusively on non-obvious, project-specific, or consistency-critical guidance.
- Explicitly state HITL gates for any action that touches production code, Git, health information, cultural content, funding claims, or external systems.
- For Whānau Hub or Māori-data related skills: require Te Tiriti-aligned reasoning, clear disclaimers, and design for cultural review.

## 8. HITL & Safety Integration

Any skill that can:

- Write or edit production code
- Touch GitHub state
- Generate health, funding, or cultural content
- Affect data sovereignty or external systems

**must** include explicit human approval gates. Reference `aether-core` and `aether-hitl-protocol`.

Default posture: agents inform, draft, prepare, and remind. Humans approve, sign, file, send, and pay.

Treat skills that contain executable scripts the same way a responsible team treats any software dependency — review before first use.

## 9. Validation Checklist Before Shipping a Skill

- [ ] Description alone is sufficient for the agent to decide when to load it.
- [ ] Description is precise (avoids vague or overly broad triggers).
- [ ] Body is under ~5k tokens; bulk moved to references/.
- [ ] HITL gates are explicit where required.
- [ ] Cultural / health / sovereignty constraints are stated if relevant.
- [ ] Skill has been generated or refined from at least one successful real run.
- [ ] A failure case has been fed back and the skill updated (or documented as still needed).
- [ ] Directory name matches the `name` field.
- [ ] CHANGELOG.md exists for any skill past v0.1.

## 10. Anti-Patterns

- Always-on large context files instead of progressive skills.
- Writing skills purely from theory without a successful run.
- Putting the “when to use” signal only in the body.
- Vague or incomplete descriptions that prevent reliable triggering.
- Overly long SKILL.md files without progressive disclosure.
- Skills that lack HITL for high-stakes actions.
- Creating skills for things the base model already does well.

## Quick Start Commands (after skill is written)

```bash
# Validate structure
./scripts/validate-skill.sh path/to/skill-name

# Or via Python helper if available
python scripts/validate_skill.py path/to/skill-name
```

After validation, the skill is ready to be placed under `skills/` (or `aether/bundled_skills/`) and will be auto-discovered by the Aether skill loader.
