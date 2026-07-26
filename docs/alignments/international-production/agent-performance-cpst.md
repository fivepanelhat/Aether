# Agent Performance & Cost-per-Successful-Task

**Primary sources**
- AIMultiple — AI Agent Performance: Success Rates & ROI (updated Jun 2026)  
  https://aimultiple.com/ai-agent-performance
- Factory × LangChain interview with Eno Reyes (16 Jul 2026)  
  https://youtu.be/HbUznYhKFOc
- Arize + Fireworks CPST study (Jul 2026)

---

## Key Evidence We Use

| Finding | Source | How we use it |
|---------|--------|---------------|
| Real-world success follows exponential decay | AIMultiple | Performance half-life metric |
| Cost-per-successful-task is the correct unit-economics measure | AIMultiple + Factory | Core metric in `aether-agent-performance` |
| Production missions can cost $100–$1,000 yet still beat human cost when success rate is acceptable | Factory / LangChain | Tokenomics notes |
| Benchmarks have short half-lives (often 3–6 months) | Multiple | Prefer continuous internal measurement |

---

## Reinforcement Videos / Links

1. AIMultiple Agent Performance page (primary text + tables)
2. LangChain × Eno Reyes — “The best AI agents cost less than you think”  
   https://youtu.be/HbUznYhKFOc

---

## CAT Skill

`aether-agent-performance` (experimental v0.1.2) encodes these findings as operational principles and metrics.
