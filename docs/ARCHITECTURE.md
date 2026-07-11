# Aether Architecture

This document describes the high-level architecture of Aether.

## Core Components

### Orchestrator
The central coordinator. It manages:
- Task state
- ReAct reasoning loop
- Tool and skill selection
- Execution flow
- Human-in-the-Loop gates

### Memory
Stores task history, decisions, and context across sessions. Supports persistence to disk.

### Guardrails
Enforces safety rules including:
- Human approval requirements for high-risk actions
- Cultural sensitivity checks
- Basic security constraints

### Tools
Modular capabilities the orchestrator can call, such as:
- Searching the codebase
- Reading files
- Querying memory
- Listing directories
- Writing files (with approval)

### Skills
Reusable, versioned units of knowledge and behavior. Skills can be:
- Suggested automatically based on the goal
- Loaded and executed during the ReAct loop
- Extended with custom execution logic

#### Governance Layer
Aether includes a top-level governance skill (`cat-architectural-standards`) that defines:
- Gold / Platinum / Diamond maturity tiers for solution quality and operational readiness
- Decision protocol and Human-in-the-Loop (HITL) gates for high-impact actions
- Te Mana Raraunga and Te Tiriti overlays for cultural safety and data sovereignty alignment

This governance layer is intended to be applied before implementation and release workflows.

## Data Flow

1. User starts a task with a goal
2. Orchestrator suggests relevant skills
3. ReAct loop begins:
   - Reason about current state
   - Decide next action (tool or skill)
   - Execute action
   - Record result
4. Loop continues until task is complete or stopped
5. Final state and history are returned

## Design Principles

- **Sovereignty First**: Designed to run locally or in controlled environments.
- **Human-in-the-Loop**: High-impact actions require explicit approval.
- **Composability**: Skills and tools are modular and reusable.
- **Observability**: Actions, decisions, and results are logged and traceable.
- **Extensibility**: Easy to add new tools and skills over time.

## Future Considerations

- Deeper LLM integration for decision making
- More advanced execution workflows
- Potential migration to LangGraph for very complex multi-agent scenarios
- Packaging as a distributable tool

## Skills CI/CD Quality Gates

Aether now ships skills CI tooling to enforce skill quality over time:
- `.github/workflows/skills-ci.yml`
- `scripts/validate-skill.sh`
- `scripts/check-skill-versions.py`
- `scripts/generate-skills-catalog.py`

These gates validate skill frontmatter, required metadata (`version`, `description`), changelog presence for versioned skills, and automated regression tests.
