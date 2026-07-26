# Harness > Model & Agent Skills Architecture

**Primary sources**
- IBM Technology — “What AI Agent Skills Are and How They Work”  
  https://www.youtube.com/watch?v=Lg-meK5IU8Q
- IndyDevDan — harness engineering / software factory / multi-agent teams
- Andrej Karpathy — “Decade of Agents”, agentic engineering vs vibe coding, preserve human understanding
- Factory “missions” as meta-harness (via LangChain interview)

---

## Key Evidence We Use

| Finding | Source | How we use it |
|---------|--------|---------------|
| Progressive disclosure (metadata → body → references) is the efficient way to load skills | IBM Technology | Exact pattern used in Aether skill authoring |
| The harness (orchestration, tools, feedback, validation) usually matters more than the underlying model | Factory, IndyDevDan, practice | Core principle in performance skill |
| Skills are procedural memory; they should be versioned, tested, and improved from real runs | IBM + CAT practice | `aether-skill-authoring` + successful-run-to-skill workflow |
| Human understanding cannot be fully outsourced | Karpathy | Supports strong HITL and “agents inform, humans decide” |

---

## Reinforcement Videos

1. IBM Technology — What AI Agent Skills Are and How They Work  
   https://www.youtube.com/watch?v=Lg-meK5IU8Q
2. LangChain × Eno Reyes (missions / harness discussion)  
   https://youtu.be/HbUznYhKFOc
3. Selected IndyDevDan harness / multi-agent content (supporting)

---

## CAT Skills

- `aether-skill-authoring` (v1.2.0)
- `aether-agent-performance` (harness > model principle)
- Experimental controls and routing skills
