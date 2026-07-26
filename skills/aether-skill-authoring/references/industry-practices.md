# Industry Practices for Agent Skills

Reference material drawn from public explanations of the emerging agent-skills open standard (notably IBM Technology’s “What AI Agent Skills Are and How They Work”, 2026) and related frontier practice.

## Progressive Disclosure (Three Tiers)

| Tier | Content loaded | When | Typical cost |
|------|----------------|------|--------------|
| 1 – Metadata | `name` + `description` only | Always (skill catalog) | A handful of tokens per skill |
| 2 – Instructions | Full `SKILL.md` body | When the agent decides the skill matches the current request | Full body size |
| 3 – Resources | `scripts/`, `references/`, `assets/` | Only when the skill actually needs them | On demand |

This design is now the de-facto standard for keeping large skill libraries token-efficient.

## Skills as Procedural Memory

- **Semantic memory** → facts (RAG, knowledge bases)
- **Episodic memory** → past experiences (conversation / session logs)
- **Procedural memory** → *how* to do something, in what order, with what judgment → **Skills**

Skills therefore complement, rather than replace, RAG and session memory.

## Description Quality is Critical

The description is the only signal the agent sees at Tier 1.  
A vague or incomplete description leads to:

- Missed triggering (skill never loads when it should)
- Incorrect triggering (skill loads for the wrong task)

Write the description so that an LLM can reliably decide “this skill applies” from the description alone.

## Skills and Tools / MCP

Skills frequently sit *above* tools:

- Tools / MCP provide the ability to act (API calls, file operations, etc.)
- Skills provide the procedural judgment of *when* and *how* to use those tools

A well-written skill reduces the need for the agent to invent the workflow every time.

## Security Posture

Skills can contain executable scripts and can be given access to local systems, credentials, or external APIs.  

Treat every skill (especially third-party or generated ones) the same way a responsible team treats any software dependency:

- Review the full content before first use
- Prefer skills that declare their side-effects clearly
- Apply the same HITL gates already required by Aether for any skill that can write code, touch Git, or affect production systems

## Open Standard Alignment

The simple folder + `SKILL.md` structure (with optional `scripts/`, `references/`, `assets/`) is converging on an open standard (see agentskills.io and related efforts).  
Keeping Aether skills aligned with this shape maximises portability and future inter-operability.
