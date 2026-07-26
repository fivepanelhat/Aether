# Model Routing & Escalation

**Primary sources**
- Factory Router product + production numbers (2026)  
  https://factory.ai/product/router
- Arize escalation / cascading patterns
- LangChain × Eno Reyes interview  
  https://youtu.be/HbUznYhKFOc
- IndyDevDan — harness engineering & multi-agent orchestration content

---

## Key Evidence We Use

| Finding | Source | How we use it |
|---------|--------|---------------|
| Intelligent routing delivers 20–50%+ cost reduction while preserving most frontier performance | Factory (benchmark + production) | Core rationale for `aether-agent-routing` |
| Cheaper / open models frequently win on review, lint, and structured validation subtasks | Factory + practice | Escalation ladder design |
| Cost ranking must never override health, cultural, or sovereignty constraints | CAT principle | Hard rule in routing skill |
| Cascading / start-cheap-then-escalate is often the best deployable CPST pattern | Arize + practice | Recommended default ladder |

---

## Reinforcement

1. Factory Router page + June/July 2026 production numbers
2. LangChain × Eno Reyes interview (routing & tokenomics section)
3. IndyDevDan videos on harness ownership and multi-agent teams (supporting “own the harness”)

---

## CAT Skill

`aether-agent-routing` (experimental v0.1.1)
