# Concrete Escalation Ladders for Coastal Alpine Tech

These are starting points, not production-ready policies. Every ladder must be measured on cost-per-successful-task under realistic traffic before being promoted.

## 1. Whānau Preterm Support Hub (Cloud + Local Hybrid)

**Goal:** High reliability on sensitive content, low cost on routine resource and directory queries.

| Rung | Model / Target | Use for | Exit condition |
|------|----------------|---------|----------------|
| 0 | Local / small open-weight (or cached responses) | Static resource lookup, FAQ, directory search | Exact match or high embedding similarity |
| 1 | Mid-tier capable model | Synthesis of multiple resources, personalised suggestions | Structured output validates + confidence ≥ threshold |
| 2 | Frontier model | Complex multi-resource reasoning, edge-case family situations, any content that will be shown to whānau | Human review gate for final high-stakes outputs |

**Hard rules**
- Any output that will be shown to whānau or contains health-adjacent content must pass cultural-safety and disclaimer checks regardless of rung.
- Never skip the human gate on high-stakes or ambiguous family-support content purely for cost reasons.

## 2. Edge / Platinum Edge Agents (RPi 5 + Hailo / DGX Spark)

**Goal:** Prefer local inference. Escalate off-box only when necessary and only under explicit policy.

| Rung | Target | Use for | Notes |
|------|--------|---------|-------|
| 0 | Local small model + Hailo acceleration | Sensor interpretation, simple classification, routine telemetry responses | Near-zero variable cost |
| 1 | Local mid-size model on DGX Spark (if available) | Short planning, multi-sensor fusion, local RAG | Still fully local |
| 2 | Controlled cloud escalation | Rare hard cases that local models have failed, or tasks requiring up-to-date external knowledge | Must be logged, rate-limited, and sovereignty-reviewed |

**Hard rules**
- Default is local. Cloud escalation requires explicit justification in the trajectory.
- Any data that leaves the edge node must respect Te Mana Raraunga and the consent graph.

## 3. Kaitiaki / Grant Agents

**Goal:** High accuracy on funding fit and compliance language; control cost on volume research.

| Rung | Target | Use for |
|------|--------|---------|
| 0 | Fast / cheap | Initial opportunity scanning, keyword / eligibility filters |
| 1 | Workhorse | Fit-matrix scoring, structured extraction from funder guidelines |
| 2 | Frontier + human review | Final positioning narrative, high-stakes compliance claims, any external communication |

**Hard rules**
- Any claim that will appear in a grant application or external email requires human approval.
- Routing must never optimise away the final human review step.

## 4. General Internal Aether / Night Cycle Agents

Default three-rung cascade:

1. Cheapest model that historically succeeds on this task class ≥ 70 % of the time.
2. Mid-tier model.
3. Frontier model (or human) for remaining failures and high-stakes actions.

Always stop on first verified success. Always log the path taken.

## Measurement Checklist for Any Ladder

Before promoting a ladder:

- [ ] Measured cost-per-successful-task vs single best model
- [ ] Coverage (tasks solved) vs single best model
- [ ] Escalation rate and average rungs used
- [ ] Latency impact
- [ ] Failure modes introduced by the router itself
- [ ] HITL and sovereignty constraints still enforced
- [ ] Routing decisions are logged for later trajectory capture
