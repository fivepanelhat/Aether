# Core Concepts — Aether Graph Engineering

## 1. Agent Graphs vs Knowledge Graphs vs Consent Graphs

**Agent Graph**  
Orchestration of work. Nodes are roles or steps (planner, researcher, auditor, synthesizer, human). Edges are routing conditions and hand-offs. State is the accumulating context and artefacts. Primary concern: reliability, auditability, and controlled progression of tasks.

**Knowledge / Whakapapa Graph**  
Representation of relationships between entities. Nodes are people, places, knowledge items, artefacts, farms, iwi entities, etc. Edges encode meaningful connections and provenance. Primary concern: preserving context so data is never stripped of origin or relationship (Te Mana Raraunga – Whakapapa).

**Consent Graph**  
Specialised, queryable structure that records grants, purposes, scopes, collective authorities, and revocation rights. Must be checked before any node accesses personal or cultural data. Primary concern: Rangatiratanga and Kotahitanga in technical form.

These three layers are complementary. An agent graph may consult a knowledge graph and must consult a consent graph when relevant.

## 2. Shared State

State is the single source of truth for “what does the system know so far?”.  
It must be:
- Explicit and inspectable
- Checkpointable (for recovery and audit)
- Capable of carrying sovereignty metadata (sensitivity class, provenance, consent status)
- Minimised where possible (prefer references over full copies of sensitive content)

## 3. The Diamond Pattern (Common Shape)

```
          ┌─────────────┐
          │   Planner   │
          └──────┬──────┘
     ┌────────┴────────┐
     ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐
│ Spec A  │ │ Spec B  │ │ Spec C  │   ← parallel expansion
└────┬────┘ └────┬────┘ └────┬────┘
     │           │           │
     └────────┬────────┘
                 ▼
          ┌─────────────┐
          │ Checker /   │
          │ Skeptic /   │
          │ Auditor     │
          └──────┬──────┘
                 ▼
          ┌─────────────┐
          │ Synthesizer │
          └──────┬──────┘
                 ▼
          ┌─────────────┐
          │ Human Gate  │  ← HITL where cost of error is high
          └─────────────┘
```

Adapt the specialist set and the placement of the human gate to the domain and risk profile.

## 4. Mapping to CAT Maturity Standards

- **Gold**: The graph must map cleanly onto a real-world workflow (unbroken chain of responsibility).
- **Diamond**: The graph must be reliable, observable, fail-closed on sovereignty checks, and support audit.
- **Platinum**: The graph should capture intermediate artefacts and outcomes in a form that can feed the data flywheel and local improvement loops.

## 5. Sovereignty Integration Points

Every graph that handles personal, health, farm, or Māori data must:

1. Query the Consent Graph before sensitive retrieval or action (X1).
2. Pass the Runtime Sovereignty Gate before any external or off-box transfer (X2).
3. Carry provenance and sensitivity metadata on state (W1, X3).
4. Prefer local / edge execution; only consented aggregates leave the boundary.
5. Escalate to HITL L2+ for any structural change affecting location, keys, consent, or external flows.

## 6. Relationship to Existing Hub Patterns

- `src/ai/graph.ts` and Aether Summit already implement agent-graph ideas.
- Specialist fleet roles (Aroha Tohunga, Activation Auditor, Kaitiaki Crawler, etc.) are natural nodes.
- Cultural safety guardrails and medical disclaimers belong on relevant nodes or as dedicated checker nodes.
- pgvector RAG remains the primary similarity retrieval layer; knowledge graphs add relationship and authority reasoning on top.

## 7. Evolution Path

Start with one high-value workflow (e.g., support triage, grant screening, or content production).  
Draw the graph manually.  
Run it with separate lanes or files.  
Only after the structure proves useful, promote it to LangGraph or equivalent with formal state and HITL interrupts.  
Document the graph and its consent/sovereignty requirements so it can be reused and audited.
