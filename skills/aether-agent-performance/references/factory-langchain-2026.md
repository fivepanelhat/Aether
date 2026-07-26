# Factory × LangChain Interview Notes — 16 July 2026

**Source:** “The best AI agents cost less than you think”  
LangChain conversation with Eno Reyes (Co-founder & CTO, Factory.ai)  
https://youtu.be/HbUznYhKFOc

## Why this source matters

Factory operates a production “24/7 autonomous software factory” that turns signals into deployed code. The discussion is grounded in real unit economics, routing behaviour, and long-term HITL experience rather than benchmark theatre.

## Key extractable points

### Tokenomics & Cost-per-Successful-Task
- Production missions can cost $100–$1,000 in inference.
- This is frequently still cheaper than equivalent human engineering effort when success rate and reliability are acceptable.
- The largest source of waste is over-use of expensive frontier models, not agent loops themselves.
- Intelligent model routing routinely delivers **30–50% cost reduction**.

### Routing
- Different models win on different task types.
- Cheaper / open models often outperform frontier models on review, lint-style, and structured validation subtasks.
- A cost/quality slider is a practical operator-facing pattern.
- Routing is one of the highest-leverage levers for improving real unit economics.

### Human-in-the-Loop
- Explicitly “bullish on humans in the loop for a very long time.”
- Product management does not disappear; it evolves into higher-leverage prioritisation and stewardship.
- Engineers write deterministic lint / validation rules that agents must pass.
- Aligns strongly with Aether’s non-negotiable HITL gates and Te Mana Raraunga controls.

### Harness > Model
- The orchestration layer, tools, deterministic feedback, and validation loops usually matter more than which frontier model is underneath.
- Model-independent harness is a deliberate design goal.
- Supports the emphasis in `aether-agent-performance` and `aether-eval-harness` on measurement and structure over raw model scores.

### Deterministic Feedback & “Missions”
- Agents need reliable, deterministic signals (tests, metrics, lint).
- “Missions” act as a universal meta-harness that force verifiable outcomes.
- Validators themselves need validation (“turtles all the way down”).

### Benchmarks
- Code-review and agent benchmarks frequently have short half-lives (3–6 months).
- Over-fitting to static public benches is a real production risk.
- Reinforces the performance half-life concept already encoded in this skill.

### Memory
- “Memory” is often over-used as a concept.
- Prefer explicit, structured knowledge artefacts with clear ownership and provenance over opaque long-term memory stores.

## Usage in Aether skills

- Cited in `aether-agent-performance` under Tokenomics Notes and Core Principles.
- Cited in `aether-agent-routing` under Production Evidence.
- Supports the strong HITL stance required by `aether-hitl-protocol` and Te Mana Raraunga controls.

## Status

Research notes only. Numbers and claims should be treated as directional production evidence, not as CAT’s own measured performance.
