# Aether Development Roadmap

**Sovereign Agentic Development System**  
Aligned with Te Tiriti o Waitangi and Te Mana Raraunga

---

## Overview

Aether is being built as a **lightweight, culturally grounded, self-improving agentic development orchestrator**. The goal is to reduce founder cognitive load and repetitive work while maintaining strong human oversight and cultural safety.

This roadmap reflects a **pragmatic, phased approach** — staying with a custom Python orchestrator in the short-to-medium term, with the option to adopt LangGraph later for more complex workflows.

---

## Current Status (July 2026)

| Area                    | Status          | Notes |
|-------------------------|------------------|-------|
| Core Orchestrator       | Phase B          | ReAct loop + tool calling implemented |
| Tool System             | Functional       | 4 tools (read, search, memory, write) |
| Skill System            | Good             | 5 high-value skills created |
| Logging & Tracking      | Improved         | Basic structured logging + task state |
| HITL & Guardrails       | Active           | Guardrails module + approval awareness |
| Autonomy                | Basic            | Tool selection and ReAct loop working |
| LangGraph               | Deferred         | Option for later (user preference) |

---

## Phased Roadmap

### Phase 0 – Foundation (Completed)

- Initial architecture and principles
- Core modules: Orchestrator, Memory, Guardrails
- Basic tool system
- First set of skills
- Documentation foundation (Vision, Compliance, Skill Format)

**Status**: Done

---

### Phase 1 – Capability Hardening (Current)

**Goal**: Make the orchestrator reliable and useful for real development work.

**Key Objectives**:
- Improve ReAct loop to intelligently use both tools and skills
- Add safe execution layer (controlled file writing with approval)
- Strengthen logging, tracking, and observability
- Make skill registration more dynamic
- Improve tool selection logic

**Current Focus**:
- Enhancing the ReAct loop (tools + skills)
- Adding safe file writing with HITL gates
- Better state management and logging

**Success Criteria**:
- Orchestrator can take a goal and autonomously gather information using tools
- Can suggest and load relevant skills
- Basic execution (file writing) is gated behind approval

---

### Phase 2 – Execution & Autonomy (Next)

**Goal**: Enable the orchestrator to safely generate and apply changes with minimal guidance.

**Planned Work**:
- Controlled file writing with approval workflow
- Better integration between skills and tools
- Improved decision-making in the ReAct loop
- Support for multi-step execution plans
- Basic CLI interface (`aether run`, `aether task`)

**Success Criteria**:
- User can give high-level tasks and receive proposed changes
- Clear approval gates before any file modification or Git action

---

### Phase 3 – Polish & Portability

**Goal**: Make Aether easy to use and share across projects.

**Planned Work**:
- Package as installable Python package
- Add examples and usage documentation
- Create simple CLI
- Improve error handling and user experience
- Add more skills (Design System, Release Engineering, etc.)

**Success Criteria**:
- Someone can clone the repo and start using Aether with minimal setup
- Clear examples of how to use it on real projects

---

### Phase 4 – Advanced Capabilities (Future)

**Goal**: Increase autonomy and capability while staying aligned with Aether’s principles.

**Possible Directions**:
- Deeper LLM integration for planning and tool selection
- Self-improvement loop (creating new skills from experience)
- LangGraph migration (if complexity increases)
- Multi-project memory and cross-project learning

**Note**: These are intentionally lower priority until the core experience is solid.

---

## Guiding Principles

- Stay **lightweight and sovereign** by default
- Prioritise **Human-in-the-Loop** on high-impact actions
- Embed **Te Mana Raraunga** principles in design and guardrails
- Favour **clarity and maintainability** over maximum autonomy early on
- Build for **real usage** on the Whānau Preterm Support Hub first

---

## Success Metrics (Proposed)

- Reduction in time spent on repetitive technical tasks
- Ability to complete small-to-medium tasks with minimal guidance
- Clear audit trail of decisions and tool/skill usage
- Positive feedback from actual usage on the Hub project

---

## Risks & Dependencies

- Scope creep (trying to do too much too early)
- Over-reliance on LLM capabilities before core flows are solid
- Balancing autonomy vs control (especially around file writing and Git)

---

**This is a living document.** It will be updated as priorities evolve.

Last updated: July 2026
