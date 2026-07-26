---
name: aether-agent-routing
description: Use when designing, implementing, or tuning agent or model routing strategies, escalation ladders, difficulty-based routing, or dynamic delegation for cost-per-successful-task optimisation. Handles pre-generation classification, cascading escalation, agent-as-router patterns, and experience-driven routers. Always measure impact on cost-per-successful-task and respect HITL plus sovereignty constraints. Trigger phrases include agent routing, model routing, escalation ladder, cascade models, route by difficulty, dynamic delegation, cost-aware routing.
metadata:
  version: "0.1.1"
  status: experimental
  owner: Coastal Alpine Tech
  last_updated: "2026-07-27"
  related: aether-agent-performance, aether-eval-harness, aether-trajectory-capture, aether-core, cat-architectural-standards
  source: "Arize/Fireworks CPST study (Jul 2026); Factory × LangChain interview (16 Jul 2026); Mercor, Ramp, Cursor, EvoRoute, vLLM Semantic Router patterns; CAT production needs"
---

# Aether Agent Routing

Production skill for designing and operating routing policies that improve real-world agent economics and reliability. Complements `aether-agent-performance` by providing the concrete patterns and decision rules for how models and agents are selected at runtime.

## When to Load

- Designing a new multi-model or multi-agent system.
- Tuning an existing agent to reduce cost-per-successful-task without losing coverage.
- Choosing between static, classification, cascading, or dynamic delegation approaches.
- Building escalation ladders for Hub, edge, grant, or farm agents.
- Reviewing whether current routing is helping or harming unit economics.
- Any discussion of “which model should handle this request?”

## Core Principles

1. **Route for outcomes, not tokens.** The only metric that matters is cost-per-successful-task (and secondary constraints such as latency, sovereignty, and cultural safety).
2. **Most tasks are easy.** Frontier capacity should be reserved for the long tail.
3. **Wrong cheap answers are expensive.** Prefer escalation with early exit when the cost of a silent failure is high.
4. **The router itself must be cheap.** Routing overhead must be far smaller than the savings it produces.
5. **Log everything.** Every routing decision and outcome is training data for better future routers and for trajectory capture.
6. **Constraints override cost.** Health data, cultural content, Te Mana Raraunga requirements, and HITL gates take precedence over pure cost ranking.

## Strategy Selection Guide

| Workload shape | Preferred strategy | Why |
|----------------|--------------------|-----|
| Homogeneous, stable difficulty | Static selection | Lowest complexity |
| Clear easy / medium / hard clusters | Query classification or simple cascade | Strong CPST improvement |
| Long-horizon multi-step work | Dynamic / Agent-as-Router | Keeps high-stakes decisions on strong models |
| High volume + good tracing already | Experience-driven or hybrid | Approaches oracle over time |
| Platinum Edge (local inference) | Quality / latency / sovereignty routing | Dollar cost approaches zero |

## Production Evidence (Jul 2026)

- Intelligent routing (including simple cost/quality sliders) routinely delivers 30–50% cost reduction while maintaining or improving task coverage.
- Cheaper or open-weight models frequently outperform frontier models on specific subtasks (especially review, lint-style, and structured validation work).
- The dominant waste pattern is sending routine work to the most expensive model rather than agent-loop inefficiency.
- Source notes: `aether-agent-performance/references/factory-langchain-2026.md`.

## Cascading Escalation (Recommended Default for Most CAT Agents)

Start with the cheapest model that has a reasonable chance of success. Escalate only when needed. Stop on first verified success.

**Typical three-rung ladder for cloud-backed agents:**

1. **Fast / cheap** (local or small open-weight / flash-class model) — routine classification, simple extraction, high-confidence patterns.
2. **Workhorse** (mid-tier capable model) — generation, synthesis, moderate reasoning.
3. **Frontier** — ambiguous, high-stakes, multi-step, or previously failed cases.

**Exit conditions (examples):**
- Schema / structured-output validation passes
- Confidence score above threshold
- Explicit success criteria met
- Tool-use correctness confirmed
- Human-in-the-loop not required

**Hard stop rules:**
- Never escalate past the point where human review is mandatory.
- Never route health, cultural, or sovereignty-sensitive content solely on cost.
- Always record the full escalation path for later analysis.

## Dynamic / Agent-as-Router Pattern

A capable main agent retains:
- Task decomposition and planning
- Ambiguous or high-stakes decisions
- Final review and synthesis

It delegates:
- Mechanical exploration
- Boilerplate generation
- Tool loops that are token-heavy but low-risk
- Routine verification steps

This pattern preserves quality while moving the bulk of tokens to cheaper models. It requires good observability of sub-agent outcomes.

## Measurement Requirements

Every routing policy must be evaluated on:

- Cost-per-successful-task (primary)
- Coverage / success rate vs the single best model
- Latency impact (p50 / p95)
- Escalation rate
- Failure modes introduced by the router itself

Oracle routing (perfect hindsight) provides the theoretical ceiling. Practical escalation should close most of the gap.

## HITL & Safety

- Routing decisions that affect production traffic, cost claims, or high-stakes domains require explicit approval before deployment.
- Any change to the escalation ladder or confidence thresholds for agents that touch health, cultural, or Māori data content must go through the normal cultural-safety and HITL gates.
- Routing logs are operational data; treat them under the same sovereignty rules as other system telemetry.

## Anti-Patterns

- Routing every request to the cheapest model and calling the resulting quality loss “acceptable”.
- Building a sophisticated router whose own inference cost exceeds the savings.
- Ignoring the retry tax when calculating CPST improvements.
- Treating routing as a pure cost optimisation when constraints are present.
- Failing to log routing decisions, making later improvement impossible.

## Integration

- Load `aether-agent-performance` first when the question is about overall economics or half-life.
- Use this skill when the question is specifically about how to choose or sequence models/agents.
- Successful routing policies and escalation ladders are high-value candidates for `aether-trajectory-capture`.
- On Platinum Edge, re-evaluate the entire ladder because local inference changes the cost structure.

---

Coastal Alpine Tech · Aether  
aether-agent-routing v0.1.1 · 27 July 2026
