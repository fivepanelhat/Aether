---
name: aether-agent-performance
description: Use when measuring, forecasting, or improving real-world AI agent performance, success rates, ROI, stability under change, cost-per-successful-task, or agent routing strategies. Handles performance half-life analysis, category-specific metrics, baseline setting, hybrid human-AI workflows, continuous monitoring, and model routing / escalation patterns. Always require verifiable evidence and HITL for production claims. Trigger phrases include agent performance, success rate, ROI of agents, performance half-life, agent reliability in production, cost per success, agent routing, model routing, escalation ladder.
metadata:
  version: "0.1.2"
  status: experimental
  owner: Coastal Alpine Tech
  last_updated: "2026-07-27"
  related: aether-eval-harness, aether-trajectory-capture, agent-reliability-context, aether-core, cat-architectural-standards, aether-agent-routing
  source: "AIMultiple – AI Agent Performance Success Rates & ROI (updated 23 Jun 2026); Arize/Fireworks CPST study (Jul 2026); Factory × LangChain interview (16 Jul 2026); internal CAT production patterns"
---

# Aether Agent Performance

Production-oriented skill for measuring and improving real-world agent performance. Complements `aether-eval-harness` (internal testing patterns) by encoding external benchmark insights, exponential decay behaviour, and operational practices that determine whether agents deliver ROI.

## When to Load

- Designing or reviewing success criteria for any production agent.
- Analysing why an agent’s success rate is decaying over time or across environments.
- Setting baselines before first deployment or pilot.
- Deciding between single-agent vs multi-agent / hybrid human-AI approaches.
- Forecasting cost and reliability for a new use case.
- Preparing evidence of agent reliability for investors, partners, or Night Cycle reports.
- Any discussion of “how good is this agent actually?” in real conditions.

## Core Principles

1. **Evidence over assertion.** Never claim a success rate without the underlying measurement method, sample size, and environment.
2. **Performance decays.** Real-world success rates follow an exponential decay pattern. Measure the half-life (point at which success drops to 50% of initial rate) for every important workflow.
3. **Stability under change > peak success.** An agent that scores 90% on a static benchmark but collapses on minor UI or data changes is not production-ready.
4. **Cost-per-successful-task is the real unit economics metric.** Track tokens, latency, and dollar cost only for the successful completions.
5. **HITL remains the final gate.** Evaluation informs; humans approve high-stakes outcomes. Production evidence (Factory / LangChain, Jul 2026) remains strongly bullish on humans in the loop for a long time.
6. **Harness > model.** Orchestration, deterministic feedback, and validation loops usually matter more than which frontier model sits underneath.

## Standard Metrics (Minimum Set)

Always report these when evaluating an agent or skill:

| Metric | Definition | Why it matters |
|--------|------------|----------------|
| Task Completion Rate | % of tasks that reach a correct, usable end state | Primary success signal |
| Stability under Change | Drop in success rate when interface, data, or instructions change modestly | Predicts production brittleness |
| Source Grounding / Hallucination Rate | % of claims that are correctly linked to evidence (or invented) | Critical for search, research, and high-stakes domains |
| Latency (p50 / p95) | Time to useful output | User experience and cost |
| Cost per Successful Task | Total spend (tokens + infra) divided only by successful completions | True unit economics |
| Performance Half-life | Number of runs, days, or environmental changes until success rate falls to 50% of baseline | Forecasting and maintenance planning |

Additional domain metrics live in `references/category-metrics.md`.

## Assessment Protocol (Baseline → Half-life)

1. **Map the workflow** on two axes: complexity and business value.
2. **Define observable success** for each key task (not “the agent said it was done”).
3. **Run a controlled baseline** (minimum 20–30 representative tasks) under realistic conditions.
4. **Introduce controlled variation** (UI change, new data shape, slight instruction drift) and re-measure.
5. **Calculate half-life** and surface the decay curve.
6. **Document failure modes** with concrete examples.
7. **Set monitoring thresholds** (alert when success rate drops below an agreed floor).

Never ship a production claim without at least steps 1–3 completed and recorded.

## Deployment Patterns That Improve Real-World Performance

- **Decompose complex procedures** into shorter, high-accuracy subtasks with clear hand-offs.
- **Hybrid workflows**: let the agent handle high-probability steps; require human review for low-confidence or high-stakes decisions.
- **Multi-agent architectures** with specialised agents and explicit hand-off contracts (prefer fewer, well-described skills over sprawl).
- **Continuous monitoring** with tracing, success/failure logging, and periodic human sampling.
- **Checkpoint / error-recovery systems** so a single subtask failure does not discard the entire trajectory.
- Prefer tools and models that trade a little peak speed for higher stability under change.

## Tokenomics Notes (Jul 2026)

- Real production missions can cost $100–$1,000 in inference. This is often still cheaper than the equivalent human engineering time when success rate and half-life are acceptable.
- The largest source of waste is usually **over-use of expensive frontier models**, not agent loops themselves.
- Intelligent model routing routinely delivers 30–50% cost reduction while preserving or improving coverage (Factory / LangChain evidence, Jul 2026).
- Benchmarks (especially code-review and agent suites) have short half-lives (often 3–6 months). Prefer continuous internal measurement over static public leaderboards.
- “Memory” is frequently over-used as a concept; prefer explicit, structured knowledge artefacts with clear ownership and provenance.

See `references/factory-langchain-2026.md` for the source notes.

## Routing Strategies (High-Impact Lever for CPST)

Routing is one of the strongest practical levers for improving cost-per-successful-task. Most production tasks do not require a frontier model. Good routing spends expensive capacity only where it actually improves outcomes.

### Primary Patterns

1. **Static selection** — Choose one model (or fixed mapping) after evaluating the full suite. Simple but inflexible.
2. **Query / difficulty classification (pre-generation)** — Lightweight router inspects the request and sends it to a model sized for that difficulty or domain. One call only.
3. **Cascading / escalation (post-generation)** — Start cheap. Escalate only on low confidence, validation failure, or explicit difficulty signals. Stop on first success. Often the best deployable CPST.
4. **Dynamic / Agent-as-Router** — A capable main agent keeps high-stakes planning and review, then delegates token-heavy but lower-stakes subtasks to cheaper models.
5. **Experience-driven** — Router accumulates outcome history and continuously improves its selection policy.

### Design Rules for CAT / Aether

- Always measure the effect on **cost-per-successful-task**, not average cost per attempt.
- Keep the router itself cheap and fast.
- Prefer escalation with early exit when the cost of a wrong cheap answer is high.
- Log every routing decision + outcome (feeds trajectory-capture and future self-improving routers).
- On Platinum Edge hardware the economics invert: local inference cost approaches zero, so route for latency, quality, or sovereignty rather than pure dollar cost.
- Never treat routing as a pure cost optimisation when cultural safety, health data, or sovereignty constraints are in play — those constraints override cost ranking.

Detailed patterns, empirical results, and concrete ladders live in the companion skill `aether-agent-routing` and in `references/routing-strategies.md`.

## Integration with Existing Aether Skills

- Use `aether-eval-harness` for the internal testing layers (unit, behavioural, LLM-as-judge, architecture congruence).
- Use this skill for production measurement, ROI forecasting, and half-life analysis.
- Use `aether-agent-routing` when designing or tuning the actual routing / escalation policy.
- Feed successful measured trajectories into `aether-trajectory-capture`.
- Surface half-life, cost-per-success, and routing effectiveness metrics in Night Cycle Morning Briefs when relevant.
- Apply `cat-architectural-standards` (especially Platinum Edge) when the agent runs on local hardware.

## HITL & Safety Requirements

- Any public or investor-facing success-rate claim requires explicit founder (or designated) approval.
- Never present benchmark numbers from third-party sources as CAT’s own measured performance.
- When evaluating agents that touch health, cultural, financial, or sovereignty-sensitive data, require the cultural-safety and data-sovereignty checks defined in `aether-core` and related skills.
- Evaluation results inform decisions; they do not replace approval gates for production actions, Git changes, or external communications.

## Anti-Patterns

- Reporting only peak success rates without stability or half-life data.
- Using token volume or number of searches as a proxy for quality.
- Claiming production readiness from static benchmarks alone.
- Creating new evaluation skills that duplicate `aether-eval-harness` instead of extending it.
- Accepting “the agent completed the task” without independent verification of the outcome.

## Quick Reference Commands

After any performance evaluation run:

```bash
# Record the measured numbers and half-life estimate
# (store under the relevant project’s eval/ or night-cycle/ artefacts)
```

Always pair quantitative results with at least one concrete failure example and one concrete success example.

---

Coastal Alpine Tech · Aether  
aether-agent-performance v0.1.2 · 27 July 2026
