---
name: aether-graph-engineering
description: Use when designing, reviewing, implementing, or evolving agent graphs, knowledge graphs, consent graphs, or workflow graphs for Aether, Coastal Alpine Tech, Whānau Preterm Support Hub, or Mana Kai. Handles graph engineering as managed workflows of jobs + arrows + state, separates agent graphs from knowledge/Whakapapa graphs, enforces sovereignty gates and HITL, and maps work onto Gold/Platinum/Diamond standards. Trigger phrases include graph engineering, agent graph, knowledge graph, consent graph, workflow graph, LangGraph design, graph vs chat, diamond pattern graph.
metadata:
  version: "0.1.1"
  status: active
  owner: Coastal Alpine Tech
  last_updated: "2026-08-04"
  related: aether-core, aether-data-sovereignty, te-mana-raraunga-controls, aether-whanau-hub-architecture, cat-architectural-standards, aether-hitl-protocol, aether-agent-fleet
  source: "Greg Isenberg graph engineering framing (2026); Te Mana Raraunga controls; Aether Summit + LangGraph patterns; CAT Platinum Edge"
---

# Aether Graph Engineering

Operational skill for designing and governing graphs in Coastal Alpine Tech systems. Turns one-shot AI chats into managed, auditable, sovereignty-respecting workflows.

## When to Load

- Designing or refactoring any multi-step AI workflow (support, content, coding, research, grants, farm ops, whānau support).
- Building or reviewing agent orchestration (LangGraph, custom graph.ts, Aether Summit routing).
- Implementing or auditing consent graphs, knowledge/Whakapapa graphs, or provenance graphs.
- Deciding whether a task should stay in a single chat or become a graph.
- Mapping work to Gold / Platinum / Diamond standards where relationship structure or workflow control is central.
- Any discussion of “graph engineering”, agent graphs, or moving beyond prompt/context engineering alone.

## Core Definition (CAT Version)

**Graph engineering** is the deliberate design of work as **jobs connected by arrows with shared state**, so AI systems operate as managed workflows rather than single opaque chats.

Three complementary layers exist in CAT:

1. **Agent Graphs** (workflow / orchestration)  
   How work moves: planner → parallel specialists → checker/skeptic → synthesizer → human gate.  
   Primary tools: LangGraph patterns, `src/ai/graph.ts`, Aether Summit routing.

2. **Knowledge / Whakapapa Graphs**  
   How information and entities are related: people ↔ whenua ↔ knowledge ↔ artefacts ↔ provenance.  
   Supports Te Mana Raraunga principle of Whakapapa (maintain context and relationships).  
   Complements (does not replace) vector RAG.

3. **Consent Graphs**  
   First-class, queryable artefact of who may access what, for which purpose, under whose authority, and with what revocation path.  
   Must control (X1 in te-mana-raraunga-controls). Agents check before personal or cultural data access.

Prompt engineering improves the question. Context engineering improves the information. Graph engineering improves the *structure of the work and the relationships that govern it*.

## Design Principles

- Prefer the **smallest graph** that raises quality and auditability.
- Separate writer from checker. A model grading its own output inflates confidence.
- Place human-in-the-loop gates where mistakes are expensive (health, cultural, financial, sovereignty, production code).
- Maintain shared state explicitly (what the system knows so far).
- Parallelise independent research or specialist lanes; merge before final synthesis.
- Fail closed on missing consent, residency, or sensitivity checks (runtime sovereignty gate).
- Start manual or whiteboard first; formalise only after the structure proves useful.
- Align every graph with the Cultural Safety & Sovereignty Overlay and the relevant Gold / Platinum / Diamond tier.

## Vocabulary

| Term              | Meaning |
|-------------------|---------| 
| Job / Node        | A discrete step (plan, research, check, synthesise, approve) |
| Arrow / Edge      | Dependency or routing condition |
| State             | Shared record of what is known so far (checkpointable) |
| Agent Graph       | Workflow of how work moves between roles |
| Knowledge Graph   | Relationships between entities and artefacts |
| Consent Graph     | Queryable record of permissions, purposes, and authorities |
| Diamond Pattern   | Common shape: expand (parallel) → filter/check → merge → human gate |

## When to Use a Graph vs a Single Chat

Use a graph when the work has any of:
- Multiple distinct steps or roles
- Parallel research or specialist paths
- Risk, policy, or cultural checks
- Human approval required before irreversible action
- Need for audit trail or reuse of intermediate artefacts
- Sovereignty or consent constraints

Keep a single chat for simple, low-stakes, single-pass tasks.

## Three Levels of Implementation

1. **Manual / Whiteboard**  
   Draw jobs and arrows (Excalidraw, tldraw, or paper). Run steps in separate conversation lanes or files. Lowest risk; fastest learning.

2. **File- or Repo-backed**  
   Each node writes its own artefact. State lives in the filesystem or a simple store. Easy to inspect and version.

3. **Formal Orchestration**  
   LangGraph (or equivalent) with checkpointers, conditional edges, and HITL interrupts. n8n / Make for integration with external systems. Use only after the manual structure is proven.

Always begin at Level 1 for new high-stakes graphs.

## CAT-Specific Requirements

- Load and obey `aether-data-sovereignty` and `te-mana-raraunga-controls` whenever the graph touches personal, health, farm, or Māori data.
- Consent graph check (X1) is mandatory before any node retrieves or acts on sensitive data.
- Runtime Sovereignty Gate (X2) must be consulted before any off-box or external-model transfer.
- Provenance and sensitivity metadata travel with state (W1, X3).
- HITL L2 or higher for any change that alters data location, keys, consent, or external flows.
- Cultural safety and medical disclaimers apply to any whānau-facing or health-related node outputs.
- Prefer local / edge processing; only aggregated or explicitly consented signals leave the node.

## Integration with Existing Skills

- Always consider loading `aether-core` first.
- Pair with `aether-whanau-hub-architecture` for Hub-specific graph.ts and Summit patterns.
- Pair with `aether-agent-fleet` when designing specialist roles inside an agent graph.
- Use `cat-architectural-standards` to classify the graph work (Gold workflow mapping, Platinum learning hooks, Diamond reliability).
- Use `aether-hitl-protocol` for gate levels and approval artefacts.
- Knowledge and consent graph design must reference `te-mana-raraunga-controls`.

## Anti-Patterns

- Turning every simple task into a complex graph.
- Letting a single model both produce and grade its own critical output.
- Building graphs that bypass consent or sovereignty checks for convenience.
- Claiming Te Mana Raraunga alignment without a queryable consent graph and provenance.
- Jumping straight to LangGraph without first validating the structure manually.
- Treating knowledge graphs as a replacement for vector RAG instead of a complement.
- Ignoring the Cultural Safety Overlay when the graph produces or routes content for whānau.

## Practical Starting Pattern (Diamond)

1. Planner node breaks the goal into angles or sub-jobs.
2. Parallel specialist / researcher nodes (customer, competitor, risk, cultural, technical, etc.).
3. Skeptic / checker / auditor node attacks weak findings and policy risks.
4. Merger / synthesizer produces a single coherent artefact.
5. Human gate reviews and approves (or rejects) before any irreversible action or external publication.

Adapt the specialist set to the domain (Hub support, Mana Kai redistribution, grants, coding, content).

## Related References

- `references/core-concepts.md` — expanded definitions and CAT mapping
- `references/CHANGELOG.md` — version history
- Greg Isenberg framing (agent graphs as managed work) adapted for sovereign systems

---

Coastal Alpine Tech · Aether  
aether-graph-engineering v0.1.1 · 4 August 2026
